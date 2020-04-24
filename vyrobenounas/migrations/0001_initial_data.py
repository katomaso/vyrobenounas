# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

from datetime import timedelta
from decimal import Decimal
from django.db import migrations
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils import timezone
from os import path


def checkout_forward(apps, schema_editor):
    """Forward checkout app."""
    payment_backend = apps.get_model('market', 'PaymentBackend')
    payment_backend.objects.get_or_create(
        url_name='checkout-pay-on-delivery',
        name="Hotově/bankovním převodem",
        description="Dobírka nebo osobní platba"
    )
    # PaymentBackend.objects.create(
    #     url_name='checkout-payment-mtransfer',
    #     name="Kartou (mTransfer)",
    #     description="Kreditní karta nebo bankovní převod"
    # )
    mail_model = apps.get_model('dbmail', 'MailTemplate')
    mails = {
        'checkout-confirmed-shop': dict(
            subject="Nová objednávka od {{ customer.get_full_name }}",
            context_note="{customer: 'User model instance', order: 'Order model instance'}",
            message="""    Dobrý den,
{% if customer.male %}pan{% else %}paní{% endif %} {{customer.get_full_name}}
s emailem {{ customer.email }} si ve vašem obchodu objednal{% if customer.female %}a{% endif %} zboží
{% for item in order.item_set %}
  * {{item.item_name}} {{item.quantity}}x za cenu {{item.line_total}}
{% endfor %}
Způsob dopravy byl zvolen "{{order.shipping}}". Uživateli byla připočítána
částka {{order.shipping_costs}} za dopravu.
{% if order.get_shipping_address %}
Uživatel stanovil jako svoji doručovací adresu
{{order.get_shipping_address}}
{% endif %}
Způsob úhrady byl zvolen jako {{order.payment}}.

Důležité! Až budete mít zboží připravené k vyzvednutí nebo odeslání, klikněte
u objednávky na ikonku letadla nebo na <a href="{% url checkout-order-shipped order=order.uid %}"> tento odkaz</a>.

V příloze Vám zasíláme fakturu pro zákazníka.
Můžete si ji tak vytisknout předem a připravit pro předání zboží. Fakturu dostane
zákazník také emailem hned jak dojde platba nebo označíte objednávku jako dokončenou.

Až předáte/odešlete zboží a obdržíte platbu, označte tuto objednávku jako
dokončenou v administraci vašeho obchodu {{ domain }}{% url 'admin-home' %}

    Vyrobeno u Nás"""),

        'checkout-confirmed-customer': dict(
            subject="Vaše objednávka byla předána {{ shop.name }}",
            message="""    Dobrý den,
vaše objednávka byla doručena do obchodu {{ shop.name }}.

Vámi objednané zboží v tomto obchodě je
{% for item in order.item_set %}
  * {{item.item_name}} {{item.quantity}}x za cenu {{item.line_total}}
{% endfor %}
Způsob dopravy byl zvolen {{order.shipping}}.
Způsob úhrady byl zvolen jako {{order.payment}}.

V příloze zasíláme proformu. Fakturu obdržíte od obchodníka po zaplacení
zboží.

    Vyrobeno u Nás"""),

        'checkout-completed-customer': dict(
            subject="Vyrobeno u Nás - platba pro {{ shop.name }} obdržena",
            message="""    Dobrý den,
vaše objednávka ze dne {{order.created|date:"j. E"}} v obchodě {{shop.name}}
byla v pořádku zaplacena. V příloze naleznete fakturu.

    Vyrobeno u Nás"""),
        'checkout-completed-shop': dict(
            subject="Objednávka od {{ customer.name }} zaplacena",
            message="""    Dobrý den,
objednávka od uživatele {{ customer.name }} ze dne {{order.created|date:"j. E"}}
byla v pořádku zaplacena. V příloze naleznete kopii faktury kterou obdržel zákazník.

Až odešlete zásilku resp. zákazník si zboží přebere, prosíme označte objednávku
v administraci jako odeslanou.

    Vyrobeno u Nás"""),

        'checkout-shipped-customer': dict(
            subject="Zboží odesláno/vyzvenuto z {{ shop.name }}",
            message="""{% load cz %}    Dobrý den,
vaše objednávka ze dne {{order.created|date:"j. E"}} v obchodě {{shop.name}}
byla vyzvednuta resp. odeslána, podle vaší volby.

Pokud jste neobdržel{% if_female customer.name 'a' %} fakturu, můžete si ji
kdykoli stáhnout v PDF v administraci svého účtu {{ domain }}{% url 'user-manage' %}.

    Vyrobeno u Nás""")}

    for slug, items in mails.items():
        mail_model.objects.get_or_create(name=slug, slug=slug,
                                         defaults=dict(is_html=False, **items))


def core_forward(apps, schema_editor):
    """Create basic structure of the shop."""
    # Create basic super user with bank account
    user = apps.get_model("market", "User").objects.create(
        name="Tomáš Peterka",
        email="tom@vyrobenounas.cz",
        password=make_password("ahoj"),
        is_superuser=True,
    )
    apps.get_model("account", "EmailAddress").objects.create(
        user=user,
        email=user.email,
        verified=True,
        primary=True,
    )
    apps.get_model("market", "Address").objects.create(
        name="Tomáš Peterka", user_shipping=user, user_billing=user,
        street="Zdislavická 723",
        country="Pha",
        zip_code="142 00",
        business_id="87510162",
        tax_id="CZ8909110188",
    )
    apps.get_model("market", "BankAccount").objects.create(
        user=user,
        prefix="670100", number="2206308683", bank="6210"
    )
    shop_address = apps.get_model("market", "Address").objects.create(
        name="Tomáš Peterka",
        street="Zdislavická 723",
        country="Pha",
        zip_code="142 00",
        business_id="87510162",
        tax_id="CZ8909110188",
    )
    shop_account = apps.get_model("market", "BankAccount").objects.create(
        prefix="670100", number="2206308683", bank="6210", user=None,
    )
    shop = apps.get_model("market", "Shop").objects.create(
        user=user, address=shop_address, bank_account=shop_account, active=False,
        name="Tomáš Peterka",
    )
    shop.logo = SimpleUploadedFile(
        name='shop-logo.png', content_type='image/png',
        content=open(path.join('market', 'static', "apple-touch-icon-precomposed-128.png"), "rb").read())
    shop.save()

    mail_model = apps.get_model("dbmail", "MailTemplate")
    mails = {
        "core-email-login": dict(
            subject="Váš obchod na Vyrobeno u Nás",
            message="""    Dobrý den,

uložili jsme Vaše jméno a email pro Vaše pohodlí. Chcete-li mít tyto ůdaje opět
předvyplněné, přistupte na Vyrobeno u Nás přes {{ domain }}{% url 'admin-email-login' slug=user.uid %}

Doporučujeme nastavit si heslo, aby nebylo nutné pokaždé hledat tuto zprávu.
Pokud si nastavíte heslo, můžete se pak lehce přihlásit zadáním
svého emailu {user.email} a hesla.

    Vyrobeno u Nás
"""),

        "core-password-reset": dict(
            subject="Reset hesla na Vyrobeno u Nás",
            message="""    Dobrý den,

byla vyžádána změna hesla pro váš účet.
Můžete tak učinit na {{ domain }}{% url 'account_reset_password' uid=user.uid %}

Pokud jste změnu nevyžádali, prosím ignorujte tento email a/nebo nám dejte vědět na
ahoj@vyrobenounas.cz

    Vyrobeno u Nás
"""),
        "core-shop-no-id": dict(
            subject="Váš obchod na Vyrobeno u Nás bez IČ",
            message="""    Dobrý den,

Založili jste obchod bez oficiálního IČ (identifikačního čísla) a DIČ. Proto pro Vás
máme pár cenných informací.
Pokud jste to tak nezamýšli, pak jej prosím doplňte na {{ domain }}{% url 'admin-shop' %}

Pokud opravdu nemáte oficiální IČ, pak je také vše v pořádku a můžete u nás prodávat.
Dobrá zpráva je, že z prodeje vašich výrobků neodvádíte žádnou daň. Na druhou stranu
pro Vás platí jistá omezení. Stručný přehled jak zůstat v mezích zákona jsme pro Vás
připravili na {% url 'flatpage' url='/prodej-bez-opravneni.html' %}

    Přejeme hodně zdaru,
    Vyrobeno u Nás
""")
    }
    for slug, items in mails.items():
        mail_model.objects.get_or_create(name=slug, slug=slug,
                                         defaults=dict(is_html=False, **items))


def tariff_forward(apps, schema_editor):
    """Forward Tariff app - emails and tariffs."""
    tariff_model = apps.get_model("market", "Tariff")
    # is used for tariff discount
    tariff_model.objects.create(
        name="Až 2 výrobky nebo souhrnné ceny do 2 000 Kč - zdarma.", slug="az-2-vyrobky",
        description="Tarif na vyzkoušení či pro malé výrobce. Nechceme nikoho oškubávat.",
        daily=0, quantity=2, price=Decimal('2000')
    )
    tariff_model.objects.create(
        name="Tarif od 3 do 7 výrobků nebo souhrnné ceny 7 500 Kč.", slug="az-7-vyrobku",
        description="Výborný tarif pro výrobce, kteří chtějí přímo prodávat své zboží.",
        daily=Decimal("1.83"), quantity=7, price=Decimal('7500')
    )
    tariff_model.objects.create(
        name="Tarif od 8 do 15 výrobků nebo souhrnné ceny 35 000 Kč.", slug="az-15-vyrobku",
        description="Dobré na rozjezd vlastního většího obchodování.",
        daily=Decimal("3.7"), quantity=15, price=Decimal('35000')
    )
    tariff_model.objects.create(
        name="Tarif od 16 do 30 výrobků nebo souhrnné ceny 75 000 Kč.", slug="az-30-vyrobku",
        description="Tarif vhodný pro specializované obchodníky.",
        daily=Decimal("7.8"), quantity=30, price=Decimal('70000')
    )
    tariff_model.objects.create(
        name="Tarif od 31 do 60 výrobků nebo souhrnné ceny 155 000 Kč.", slug="az-60-vyrobku",
        description="Uspokojí obchodníky s mnoha druhy českého zboží.",
        daily=Decimal("17.06"), quantity=60, price=Decimal('155000')
    )
    tariff_model.objects.create(
        name="Tarif od 61 do 100 výrobků nebo souhrnné ceny 365 000 Kč.", slug="az-100-vyrobku",
        description="Téměř velkoobchodní tarif.",
        daily=Decimal("41.16"), quantity=100, price=Decimal('365000')
    )
    tariff_model.objects.create(
        name="Tarif nad 100 výrobků", slug="nad-100-vyrobku",
        description="Neomezený tarif pro velké obchodníky.",
        daily=Decimal("119.3"), quantity=100000, price=Decimal('99999999')
    )

    mail_model = apps.get_model('dbmail', 'MailTemplate')
    mails = {
        "tariff-billed": dict(
            subject="Proforma za používání služeb Vyrobeno u Nás",
            message="""  Dobrý den,
v příloze naleznete proformu pro úhradu služeb Vyrobeno u Nás.
Pokud si přejete ukončit spolupráci, můžete tak učinit kdykoli v administraci vašeho obchodu na adrese {{ domain }}{% url "admin-home" %}.

Vyrobeno u Nás""",
        ),
        "tariff-changed": dict(
            subject="Informace o přechodu na nový tarif Vyrobeno u Nás",
            message="""{% load core_tags %}  Dobrý den,
byl vám přiřazen nový tarif podle využívání našich služeb.
Váš nový tarif je "{{ tariff.name }}" s měsíčním plněním {{ tariff.monthly|as_price }} s DPH.
{% if discounts %}Máte u nás do budoucna slevy! Konkrétně {% for dicount in dicounts%}{{discount}}{% if loop.last %}.{%else%},{%endif%}{%endfor%}{%endif%}
Více detailů najdete v ceníku služeb na adrese {{ domain }}{% url 'tariff-list' %}

S pozdravem,
Vyrobeno u Nás
""",
        ),
        "tariff-closed": dict(
            subject="Informace o ukončení zpoplatněných služeb u Vyrobeno u Nás",
            message="""{% load core_tags %}  Dobrý den,
zrušili jsme Vám všechny placené služby. Spolu s tímto emailem byste měli dostat poslední účet k
zaplacení. Děkujeme Vám za účast v projektu pro lepší čechy.

S pozdravem,
Vyrobeno u Nás
""")}
    for slug, items in mails.items():
        mail_model.objects.get_or_create(
            name=slug, slug=slug, defaults=dict(is_html=False, **items))

    # introduce free tariff for first 50 active shops
    discount, _ = apps.get_model("market", "Discount").objects.get_or_create(
        name="Prvních 50 obchodů 3 měsíce zdarma", percent=100, usages=3)
    apps.get_model("market", "Campaign").objects.get_or_create(
        code="PRVNI50", usages=50, discount=discount,
        expiration=timezone.now() + timedelta(days=365))


def category_forward(apps, schema_editor):
    """Don't use schema_editor because the IDs are not assigned then."""
    from market.core.models import Category
    categories = {
        "Auto & Moto": {
            "Automobily": None,
            "Motorky": None,
            "Díly, Tuning": None,
            "Interiér": None,
            "Elektronika": None,
            "Ostatní": None,
        },
        "Dům a Kancelář": {
            "Koupelna": {
                "Sanitární zařízení": None,
                "Vodotechnika": None,
                "Nábytek": None,
                "Světla": None,
                "Elektronika": None,
                "Dekorace, Doplňky": None,
                "Ostatní": None,
                "Obklady": None,
            },
            "Kuchyň, Jídelna": {
                "Hrnce, Nádobí": None,
                "Mísy": None,
                "Talíře": None,
                "Hrnky": None,
                "Skleničky": None,
                "Pekáče": None,
                "Tácy": None,
                "Kuchyňské potřeby": {
                    "Prostírací sety": None,
                    "Nože": None,
                    "Vařečky": None,
                    "Nabíračky": None,
                    "Krájecí podložky": None,
                    "Ostatní": None,
                },
                "Nábytek": None,
                "Spotřebiče": None,
                "Dřezy, Baterie": None,
                "Textil": None,
                "Dekorace, Doplňky": None,
                "Ostatní": None,
            },
            "Ložnice, Obývací pokoj": {
                "Nábytek": None,
                "Textil": None,
                "Matrace": None,
                "Lampy": None,
                "Dekorace, Doplňky": None,
                "Ostatní": None,
                "Pohovky": None,
                "Lustry": None,
                "Topení": None,
                "Krby, Kamna": None,
                "Podlahové krytiny": {
                    "Koberce": None,
                    "Linolea": None,
                    "Plovoucí podlahy": None,
                    "Dlaždice": None,
                    "Parkety": None,
                },
            },
            "Dveře, Zámky": None,
            "Trezory": None,
            "Čistící prostředky": None,
            "Elektronika": {
                "Alarmy, Kamery": None,
                "Hodiny, Budíky": None,
                "Foto a příslušenství": None,
                "Televize, Přehrávače": None,
                "Reproduktory, Sluchátka": None,
                "Počítače a příslušenství": None,
                "Telefony a příslušenství": None,
                "Zábavní elektronika": None,
                "Ostatní": None,
            },
            "Sklářské výrobky": None,
            "Kancelář": {
                "Papírnictví": None,
                "Šanony, Organizátory": None,
                "Nábytek": None,
                "Stoly": None,
                "Židle": None,
                "Skříně, Poličky": None,
                "Prezentační technika": None,
            },
            "Obrazy": None,
        },
        "Člověk a Relax": {
            "Drogerie": {
                "Mýdla, šampony": None,
                "Péče o zuby": None,
                "Dámská drogerie": None,
                "Pánská drogerie": None,
                "Bylinné přípravky": None,
            },
            "Léčba": {
                "Čaje": None,
                "Mastičky": None,
                "Kapky": None,
                "Oleje": None,
            },
            "Svíčky": None,
            "Hračky": {
                "Pro nejmenší": None,
                "Pro děti": None,
                "Pro dospělé": None,
                "Dětské atrakce": None,
                "Ostatní": None,
            },
            "Párty": {
                "Kostýmy": None,
                "Ptákoviny": None,
                "Pyrotechnika": None,
                "Výzdoba": None,
                "Ostatní": None,
            },
            "Hudební nástroje": None,
        },
        "Jídlo a Nápoje": {
            "Koření": None,
            "Maso, Uzeniny": None,
            "Mléčné výrobky": None,
            "Med": None,
            "Ovoce": None,
            "Zelenina": None,
            "Sladkosti": None,
            "Nápoje": {
                "Alkoholické": None,
                "Bylinné": None,
                "Mléčné": None,
                "Nealkoholické": None,
            },
        },
        "Oblečení a Obuv": {
            "Dětské oblečení": {
                "Dupačky": None,
                "Čepice, Rukavice": None,
                "Trička, Košile": None,
                "Kalhoty": None,
                "Kraťasy, Sukýnky": None,
                "Bundy": None,
                "Overally": None,
                "Spaní": None,
            },
            "Pánské oblečení": {
                "Spodní prádlo": None,
                "Domácí": None,
                "Společenské": {
                    "Saka": None,
                    "Smokingy": None,
                    "Košile": None,
                    "Kravaty, Motýlci": None,
                    "Doplňky": None,
                    "Klobouky": None,
                },
                "Čepice, Rukavice, Šály": None,
                "Trička": None,
                "Košile": None,
                "Mikiny": None,
                "Svetry": None,
                "Kraťasy": None,
                "Kalhoty": None,
                "Bundy": None,
                "Kabáty": None,
                "Spaní": None,
                "Ostatní": None,
            },
            "Dámské oblečení": {
                "Spodní prádlo": None,
                "Domácí": None,
                "Šaty": {
                    "Letní": None,
                    "Plesové": None,
                    "Svatební": None,
                    "Ostatní": None,
                },
                "Halenky": None,
                "Sukně": None,
                "Doplňky": None,
                "Klobouky": None,
                "Čepice, Rukavice, Šály": None,
                "Trička": None,
                "Košile": None,
                "Mikiny": None,
                "Svetry": None,
                "Kalhoty": None,
                "Kraťasy": None,
                "Spaní": None,
                "Ostatní": None,
            },
            "Pánská obuv": {
                "Pantofle": None,
                "Sandály": None,
                "Vycházková": None,
                "Společenská": None,
                "Zimní": None,
            },
            "Dětská obuv": {
                "Na doma": None,
                "Na ven": None,
                "Na zim": None,
            },
            "Dámská obuv": {
                "Pantofle": None,
                "Sandály": None,
                "Vycházková": None,
                "Společenská": None,
                "Zimní": None,
            },
            "Hodinky": None,
            "Šperky": {
                "Zlato": None,
                "Stříbro": None,
                "Chirurgická ocel": None,
                "Bižuterie": None,
            },
        },
        "Sport": {
            "Baťohy": None,
            "Oblečení": {
                "Trika a košile": None,
                "Mikiny a svetry": None,
                "Kalhoty": None,
                "Doplňky": None,
            },
            "Obuv": {
                "Běžecká": None,
                "Turistická": None,
            },
            "Bruslení": None,
            "Kola": {
                "MTB": None,
                "Městská": None,
                "Silniční": None,
                "Dětská": None,
                "Elektrokola": None,
                "Nářadí": None,
                "Součástky": None,
            },
            "Plavání": None,
            "Golf": None,
            "Horolezectví": None,
            "Turistika": {
                "Stany": None,
                "Spacáky": None,
                "Ostatní": None,
            },
            "Rybaření": None,
            "Míče": None,
            "Tenis": None,
            "Zimní sporty": None,
            "Žonglování": None,
            "Ostatní": None,
        },
        "Řemesla": {
            "Šití, Pletení": {
                "Vlny": None,
                "Bavlnky": None,
                "Nitě": None,
                "Jehly, jehlice": None,
                "Látky": None,
            },
            "Pracovní nástroje": {
                "Pily": None,
                "Kladiva": None,
                "Šroubováky": None,
                "Oblečení": None,
                "Nůžky": None,
                "Rukavice": None,
                "Klíče": None,
                "Kleště": None,
                "Sekery": None,
                "Kadeřnické nástroje": None,
                "Truhlářské nátroje": None,
                "Kožedílnické nástroje": None,
                "Zednické nástroje": None,
                "Zámečnické nástroje": None,
                "Pro úklid": None,
                "Rýče, Motyky": None,
                "Kosy, Srpy, Hrábí": None,
            },
            "Stavebnictví": {
                "Barvy": None,
                "Omítky": None,
                "Dlaždice": None,
                "Betony": None,
                "Cihly": None,
                "Prkna": None,
                "Nosné prvky": None,
                "Střešní krytiny": None,
                "Spojovací materiál": None,
                "Okapy": None,
                "Komínové vložky, Tvarovky": None,
                "Zábradlí": None,
            },
            "Zahradnictví": {
                "Rostliny": None,
                "Květináče, Truhlíky": None,
                "Půda": None,
                "Hnojivo": None,
                "Hubitelé": None,
                "Sekačky, Křovinořezy": None,
                "Ploty": None,
                "Dekorace": None,
                "Zahradní domky": None,
                "Zahradní nábytek": None,
                "Grily, Udírny": None,
                "Žebříky": None,
                "Košíky": None,
            },
            "Chovatelství": {
                "Užitková zvířata": None,
                "Krmivo": None,
                "Ostatní": None,
            },
            "Zbraně": {
                "Chladné": None,
                "Historické": None,
                "Plynové": None,
                "Střelné": None,
            }
        }
    }

    def create_category(parent, names):
        if names is None:
            return
        for name in names.keys():
            category = Category.objects.create(name=name, parent=parent)
            assert category.id is not None
            create_category(category, names[name])

    create_category(None, categories)
    Category.objects.create(name="Vše ostatní", ordering=2)


def pages_forward(apps, schema_editor):
    """Forward Pages - imprint initial_data/flatpages/<LANGCODE>/*html into db.

    Use name as url, first line as title and the rest as text body.
    """
    from django.contrib.sites import models as sites_models
    from django.contrib.flatpages import models as pages_models
    # we have to use concrete models because of M2M relation

    def get_extends(s):
        matches = re.search(r"extends '|\"([^\"']+)\"|'", s)
        return matches.group(1)

    for site_code in settings.SITES:
        pagepath = path.join(
            settings.APP_ROOT, 'migrations', 'initial_data', 'flatpages', site_code)
        site, _ = sites_models.Site.objects.get_or_create(
            name=site_code, defaults={'domain': settings.SITES[site_code]})
        for pageurl in os.listdir(pagepath):
            data = open(path.join(pagepath, pageurl))
            pagetitle = data.readline().strip()[2:-2].strip()  # remove comment tags
            pagecontent = data.read()
            if "extends" in pagecontent[:15]:
                newline = pagecontent.find("\n")
                extends = get_extends(pagecontent[:newline])
                pagecontent = pagecontent[newline:]
            else:
                extends = 'flatpages/default.html'  # flatpages default
            data.close()
            instance = pages_models.FlatPage.objects.create(
                url="/" + pageurl,  # keep .html in the url
                title=pagetitle,
                content=pagecontent,
                enable_comments=True,
                template_name=extends,
                registration_required=False
            )
            instance.sites.add(site)


class Migration(migrations.Migration):
    """Data migration specific for Czech republic."""

    dependencies = [
        ('dbmail', '__latest__'),
        ('account', '__latest__'),
        ('market', '0002_foreign_keys'),
        ('flatpages', '__latest__'),
    ]

    operations = [
        migrations.RunPython(category_forward),
        migrations.RunPython(core_forward),
        migrations.RunPython(checkout_forward),
        migrations.RunPython(tariff_forward),
        migrations.RunPython(pages_forward),
    ]
