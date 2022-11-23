import argparse
import sys

supported_keywords = ["$gt","$lt","$and","$not","$or","$ne"]   
not_supported_keywords=["$set","$avg","$count","$first","$geonear","$group","$limit","$lookup","$match","$max","$merge","$min","$out","$project","$redact","$skip","$sort","$sum","$unionwith","$unset","$unwind","$cmp","$abs"]

def main(argv):
    parser=argparse.ArgumentParser()
    parser.add_argument("--file",dest="file",help="Set the MongoDB log file to analyze")

    argv = parser.parse_args()

    if argv.file is None:
        parser.error("--file is required")

    mongo_log = read_log(argv.file)
    supported_dictionary,not_supported_dictionary = search(mongo_log)
    generate_report(supported_dictionary,not_supported_dictionary)


def read_log(file):
    with open(file, 'r') as f:
        text = f.readlines()
        return text


def search(input_file):

    supported_dictionary = dict()
    not_supported_dictionary = dict()

    for line in input_file:
        for keyword in supported_keywords:
            if keyword.lower() in line:
                if not keyword in supported_dictionary:
                   supported_dictionary[keyword.lower()]=1
                else:
                   supported_dictionary[keyword.lower()]+=1

        for keyword in not_supported_keywords:
            if keyword.lower() in line:
                if not keyword in not_supported_dictionary:
                   not_supported_dictionary[keyword.lower()]=1
                else:
                   not_supported_dictionary[keyword.lower()]+=1


    return supported_dictionary,not_supported_dictionary




def generate_report(supported_dictionary,not_supported_dictionary):
    total= sum(supported_dictionary.values()) + sum(not_supported_dictionary.values())
    total_supported=sum(supported_dictionary.values())
    total_not_supported=sum(not_supported_dictionary.values())
    perc=round(total_supported/total*100)
    
    with open('report_advisor.txt','w') as f: 
        f.write("Report Summary: " +"\n")
        f.write("*****************************" +"\n")
        f.write("Your application is: " + str(perc)+"% compatible with MongoDB API\n")
        f.write("Total Aggregation Pipelines found: " + str(total)+"\n")
        f.write("Total Supported Aggregation Pipelines: " + str(total_supported)+"\n")
        f.write("Total Not Supported Aggregation Pipelines: " + str(total_not_supported)+"\n\n\n")
        


        f.write("List of supported Aggregation opperators and the number of time it appears: \n")
        f.write("********************************************************************************" +"\n")
        f.write(str(supported_dictionary)+"\n\n\n")
        

        f.write("List of NOT supported Aggregation opperators and the number of time it appears: \n" )
        f.write("********************************************************************************" +"\n")
        
        f.write(str(not_supported_dictionary)+"\n\n\n")
        #w.writerows(output_dict.items())


if __name__ == "__main__":
    main(sys.argv[1:])