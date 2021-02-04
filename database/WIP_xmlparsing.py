"""Description."""
import xmlschema as xml

schema = xml.XMLSchema(r"C:\Users\Tubsp\OneDrive\Skrivebord\Thesis\VMT\database\tmx\BSDF-v1.7.5.xsd")


schema.is_valid(r"C:\Users\Tubsp\OneDrive\Skrivebord\Thesis\VMT\database\tmx\00001\00001.xml")

schema.validate(r"C:\Users\Tubsp\OneDrive\Skrivebord\Thesis\VMT\database\tmx\00001\00001.xml")

out = schema.to_dict(r"C:\Users\Tubsp\OneDrive\Skrivebord\Thesis\VMT\database\tmx\00001\00001.xml")



#%%

import xml.etree.ElementTree as ET
tree = ET.parse(r"C:\Users\Tubsp\OneDrive\Skrivebord\Thesis\VMT\database\tmx\00001\00001.xml")
root = tree.getroot()

root.findall("WavelengthData")

root.tag
root.attrib

for child in root:
	print(child.tag, child.attrib)
	
for subchild in root[1]:
	print(subchild.tag, subchild.attrib)
	
#%%

import numpy as np
xml_data = []

xml_path = r"C:\Users\Tubsp\OneDrive\Skrivebord\Thesis\VMT\database\tmx\00002\00002.xml"
with open(xml_path, "r") as infile:
	xml_file = infile.readlines()

for i in range(len(xml_file)):
	if "<WavelengthData>" in xml_file[i]:
		data = []
		data.append(xml_file[i+2].split(">")[1].split("<")[0])
		data.append(xml_file[i+6].split(">")[1].split("<")[0])
		array = np.zeros((145, 145))
		for j in range(145):
			array[j,:] = np.array(xml_file[i+11+j].split(", ")[0:145]).astype(np.float)
		
		data.append(array)
		xml_data.append(data)
		i += 157
		


#%%

theta_bands = np.array([0,5,15,25,35,45,55,65,75,90])
number_of_azimuth_division = np.array([1,8,16,20,24,24,24,16,12])
assert number_of_azimuth_division.sum() == 145, "There should be 145 Klems patches"


solid_angles = []

for i in range(len(number_of_azimuth_division)):
	theta_HI = theta_bands[i]
	theta_LO = theta_bands[i+1]











