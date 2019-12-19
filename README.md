# Data-Analytics-On-JSON-Dumps
Compared two json dumps and extratced information using unique keys, etc..                                                                                                             
Simple Analytics Program:                                                                                                                       
* Loaded the data from both .json files

* Created two sets of unique URLH for both files and found the overlapping URLHs checking the URLHs in set one that are in set two and then the URLHs in set two that are in set two and combining them.
* Created two dictionaries with overlapped URLH and their price_available and then calculated their difference to find if there was any differnec in price.
* Created two sets of unique categories and found the length of sets.
* Found the no: of categories that are in set one but not in set two and also the categories that are in set two but not in set one and and combining them.
* Created a list of categories and sub-categories. Created another list of category-subcategory combination. Then found out the number of occurances of each taxonomy.
* Calculated the total mrp sum which are not 0 or None or even if key isn't available. In the later case the value is set as 'NA'. Then all the non-'NA' values are normalized by dividing by total sum. Then these mrp values in stored in a file 'mrp_normalized'. 
  
