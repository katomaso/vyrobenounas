
# class ImportXML(models.Model):
#     """
#     Importovat pouze zbozi, ktere ma vyrobce v seznamu ceskych vyrobcu

#     TODO: Udelat jako moznost zrusit kontrolu?
#     """
#     XML_TYPES = enumerate(("Seznam XML', 'Vyrobenounas XML"), start=1)

#     xmltype = models.SmallIntegerField(default=1, choices=XML_TYPES)
#     xmlhash = models.CharField(max_length=100)

#     vendor = models.ForeignKey(Vendor, verbose_name=_("Vendor where belongs"))
#     link = models.URLField(verbose_name=_("Link to the XML file"))  # verify_exists=True,
#     checked = models.DateTimeField(auto_now_add=True, blank=True)
#     items = models.IntegerField(default=0, blank=True)
#     category = models.ForeignKey('market.Category',
#                                  verbose_name=_("Category of products"),
#                                  help_text=_("Will be used if automatic parsing fails."))


# class ImportLog(models.Model):
#     STATUS_SUCCESS = 'success'
#     STATUS_PENDING = 'pending'
#     STATUS_FAILED = 'failed'
#     STATUSES = (
#         (STATUS_SUCCESS, _(STATUS_SUCCESS)),
#         (STATUS_PENDING, _(STATUS_PENDING)),
#         (STATUS_FAILED, _(STATUS_FAILED)),
#     )
#     import_xml = models.ForeignKey(ImportXML, null=False)
#     date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=15, null=False, choices=STATUSES, default=STATUS_SUCCESS)
#     message = models.TextField(null=True, blank=True)
