from dbdv2.data_access.pdf_reader import DbdPDFReader

b = DbdPDFReader('asfd')
a = '21/1/2563'

print(b.date_convert(a))
