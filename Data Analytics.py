import json
import gzip


class Operations:
	"""docstring for Operations"""
	def __init__(self):
		super(Operations, self).__init__()
		
	def unique_url_set(self, data):
		s = set()		
		for item in data:
			s.add(item['urlh'])
		return s	

	def url_price_dict(self, data):
		dicts = {}
		for item in data:
			if item['urlh'] in urlh_overlap and item['urlh'] not in dicts:
				if item['http_status'] == '200' and item['available_price'] == None:
					dicts[item['urlh']] = 'NA'
				else:
					dicts[item['urlh']] = float(item['available_price'])
		return dicts

	def unique_category(self, data):
		c = set()
		for item in data:
			c.add(item['category'])
		return c

	def taxon_list(self, data, tax):
		new_taxon = []
		for item in data:
			new_taxon.append(item['category'])
			new_taxon.append(item['subcategory'])
			tax.append(new_taxon)
			new_taxon = []
		return tax	

	def calculate_mrp_total(self, data, total):
		for item in data:
			if item['mrp'] == "null" or item['mrp'] == '0' or item['mrp'] == None:
				total.append('NA')
			else:	
				total.append(float(item['mrp']))
		return total			

# Load the first set of data  
data_one = []
with gzip.open("t.json.gz", "rt", encoding="utf-8") as f:
	for line in f:
		data_one.append(json.loads(line))		

# Load the second set of data
data_two = []
with gzip.open("y.json.gz", "rt", encoding="utf-8") as f:
	for line in f:
		data_two.append(json.loads(line))	

op = Operations()

s_one = op.unique_url_set(data_one)
s_two = op.unique_url_set(data_two)
					
# Counting no: of overlapping URLH
urlh_overlap = set()
for item in s_one:
	if item in s_two:
		urlh_overlap.add(item)
for item in s_two:
	if item in s_one:
		urlh_overlap.add(item)		
print("No: of overlapping URLH : {}".format(len(urlh_overlap)))

# Calculate the price difference if there is any between yesterday's and today's crawls	
dict_one = op.url_price_dict(data_one)
dict_two = op.url_price_dict(data_two)					
			
for url in dict_one:
	if url in dict_two:
		if dict_one[url] != 'NA' or dict_two[url] != 'NA':
			price_difference = dict_one[url] - dict_two[url]
			if price_difference > 0:
				print("Price increased by {0:.2f}".format(price_difference))
			elif price_difference < 0:
				print("Price decreased by {0:.2f}".format(abs(price_difference)))
			else:
				print("Price remained the same")
		else:
			print("Price of item not available")				

# Conting no: of unique categories in both files
c_one = op.unique_category(data_one)
print("No: of unique categories in todays file : {}".format(len(c_one)))
c_two = op.unique_category(data_two)
print("No: of unique categories in yesterdays file : {}".format(len(c_one)))

# List of categories that don't overlap
category_not_overlap = set()
for item in c_one:
	if item not in c_two:
		category_not_overlap.add(item)
for item in c_two:
	if item not in c_one:
		category_not_overlap.add(item)		
if len(category_not_overlap) == 0:
	print("Every category overlaps")
else:
	print("List of categories which is not overlapping : ")	
	print(category_not_overlap)

# Generate the stats with count for all taxonomies		
taxon = []
taxon = op.taxon_list(data_one,taxon)
taxon = op.taxon_list(data_two,taxon)

unique_taxon = []
for [x,y] in taxon:
	if [x,y] not in unique_taxon:
		unique_taxon.append([x,y])

for [x,y] in unique_taxon:
	print(x + " > " + y + ": {}".format(taxon.count([x,y])))

# Generate a new file where mrp is normalized.
mrp_total = []
mrp_total = op.calculate_mrp_total(data_one,mrp_total)
mrp_total = op.calculate_mrp_total(data_two,mrp_total)

mrp_sum = 0
for mrp in mrp_total:
	if mrp != 'NA':
		mrp_sum += mrp

for i,mrp in enumerate(mrp_total):
	if mrp != 'NA':
		mrp_total[i] = "{0:.5f}".format(mrp_total[i]/mrp_sum)

file = open('mrp_normalized.txt','w')
for mrp in mrp_total:
	file.write(str(mrp))
	file.write("\n")
file.close() 
