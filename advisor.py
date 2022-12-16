import argparse
import sys

supported_keywords = ["$gt","$gte","$lt","$and","$not","$or","$nor","$ne","$eq","$in","$lte","$nin","$exists","$type","$regex","$text","$near","$nearSphere","$size","$natural","$inc","$min","$max",
                        "$rename","$set","$addToSet","$pop","$pull","$push","$pullAll","$each","$position","$sort","$bit","$count","$limit","$match","$skip","$slice"]   
not_supported_keywords=["$expr","$jsonSchema","$mod","$geoIntersects","$geoWithin","$box","$center","$centerSphere","$maxDistance","$minDistance","$polygon","$all","$bitsAllClear","$bitsAllSet","$bitsANyClear",
                        "$bitsAnySet","$elemMatch","$rand","$currentData","$mul","$setOnInsert","$abs","$accumulator","$acos","$acosh","$addFields","$bucket","$bucketAuto","$changeStream","$collStats"
                        ,"$currentOp","$densify","$documents","$facet","$fill","$geoNear","$graphLookup","$group","$indexStats","$lookup","$merge","$out","$project","$redact","$replaceRoot","$replaceWith","$sample"
                        ,"$search","$searchMeta","$setWindowFields","$sortByCount","$unionWith","$unset","$unwind","$add","$allElementsTrue","$anyElementTrue","$arrayElemAt","$arrayToObject","$asin","$asinh"
                        ,"$atan","$atan2","$atanh","$avg","$binarySize","$bottom","$bottomN","$bsonSize","$ceil","$cmp","$concat","$concatArrays","$cond","$convert","$cosh","$cosh","$covariancePop","$covarianceSamp"
                        ,"$dateAdd","$dateDiff","$dateFromParts","$dateFromString","$datesubtract","$dateToParts","$dateToString","$dateTrunc","$dayOfMonth","$dayOfWeek","$dayOfYear","$degreesToRadians","$denseRank"
                        ,"$derivative","$divide","$documentNumber","$exp","$expMovingAvg","$filter","$first","$firstN","$floor","$function","$getField","$hour","$ifNull","$indexOfArray","$indexOfBytes","$indexOfCP"
                        ,"$integral","$isArray","$isNumber","$isoDayOfWeek","$isoWeek","$isoWeekYear","$last","$lastN","$let","$linearFill","$literal","$ln","$log","$log10","$ltrim","$map","$maxN","$mergeObjects"
                        ,"$meta","$minN","$millisecond","$minute","$month","$multiply","$objectToArray","$pow","$radiansToDegrees","$range","$rank","$reduce","$regexFind","$regexFindAll","$regexMatch","$replaceOne"
                        ,"$replaceAll","$reverseArray","$round","$rtrim","$sampleRate","$second","$setDifference","$setEquals","$setField","$setIntersection","$setIsSubset","$setUnion","$shift","$sin","$sinh"
                        ,"$sortArray","$split","$sqrt","$stsDevPop","$stsDevSamp","$strLenBytes","$strcasecmp","$strLenCP","$substr","$substrCP","$subtract","$sum","$switch","$tan","$tanh","$toBool","$toDate"
                        ,"$toDecimal","$toDouble","$toInt","$toLong","$toObjectId","$top","$topN","$toString","$toLower","$toUpper","$tsIncrement","$tsSecond","$trim","$trunc","$unsetField","$week","$year","$zip"]

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
            if keyword in line:
                if not keyword in supported_dictionary:
                   supported_dictionary[keyword]=1
                else:
                   supported_dictionary[keyword]+=1

        for keyword in not_supported_keywords:
            if keyword in line:
                if not keyword in not_supported_dictionary:
                   not_supported_dictionary[keyword]=1
                else:
                   not_supported_dictionary[keyword]+=1


    return supported_dictionary,not_supported_dictionary




def generate_report(supported_dictionary,not_supported_dictionary):
    total= sum(supported_dictionary.values()) + sum(not_supported_dictionary.values())
    total_supported=sum(supported_dictionary.values())
    total_not_supported=sum(not_supported_dictionary.values())
    if total==0:
        perc=0
    else:
        perc=round(total_supported/total*100)
    
    with open('report_advisor.txt','w') as f: 
        f.write("Report Summary: " +"\n")
        f.write("*****************************" +"\n")
        f.write("Your application is: " + str(perc)+"% compatible with MongoDB API\n")
        f.write("Total Aggregation Pipelines found: " + str(total)+"\n")
        f.write("Total Supported Aggregation Pipelines: " + str(total_supported)+"\n")
        f.write("Total Not Supported Aggregation Pipelines: " + str(total_not_supported)+"\n\n\n")
        


        f.write("List of supported Agregation opperators and the number of times it appears: \n")
        f.write("********************************************************************************" +"\n")
        f.write(str(supported_dictionary)+"\n\n\n")
        

        f.write("List of NOT supported Agregation opperators and the number of times it appears: \n" )
        f.write("********************************************************************************" +"\n")
        
        f.write(str(not_supported_dictionary)+"\n\n\n")
        #w.writerows(output_dict.items())


if __name__ == "__main__":
    main(sys.argv[1:])