# Misc

No guarantees on functionality!

---

* createMaiMLFile.py
    1. Function to create a MaiML file from a dictionary type:(writeContents)
    2. Function to generate a dictionary from a MaiML file:(readFile)
    3. Function to generate MaiML data of global element type:(writeGlobalContents)
    4. Function to generate MaiML data of general-purpose data container type:(writeGenericdataContainer)
    5. Function to generate MaiML data for template elements:(writeTemplates)
    6. Function that generates MaiML data for instance elements:(writeInstanceData)
    7. Function to generate MaiML data for \<chain> element:(writeChainContents)
    8. Function to generate MaiML data for \<parent> element:(writeParentContents)
    9. Function to generate MaiML data of reference element type:(writeReferenceContents)
    10. Function to generate MaiML data for \<document> element:(createDocumentContents)
    11. Function to generate MaiML data for \<protocol> element:(createProtocolContents)
    12. Function to generate MaiML data for \<data> element:(createDataContents)
    13. Function to generate MaiML data for \<eventLog> element:(createEventLogContents)
* filehash.py
    1. Program to find the hash value of a file
* tiffTest.py
    1. Function to read multi TIFF:(readTIFF1)
    2. Function to get metadata from TIFF file:(readTIFF2)
* xmltodicttocsv.py
    1. A function that retrieves all files existing in the INPUT directory and converts them to python dict type:(readfiles)
    2. Function to output python dict type data to CSV format file output.csv:(makecsv)
* xmltodicttojson.py
    1. A program that converts XML format data to python dict type data, and then converts it to JSON format data.
* yamltomaiml.py
    1. Function to obtain MaiML format data from YAML format data:(getDocment1)
