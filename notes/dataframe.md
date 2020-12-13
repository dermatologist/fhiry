
* https://stackoverflow.com/questions/63224694/converting-a-ndjson-to-csv-in-python
```
import json
import pandas as pd
with open('json_in.json', 'r') as f:
    json_in=f.read()

json_in=json.loads(json_in)

#json_in={"campaignTitle": "Template Campaign", "listName": "Trial", "leadId": 573, "timezone": "Australia/Sydney", "isComplete": 0, "customerKey": "576", "phone1": "+61212345678", "phone2": "", "phone3": "", "leadUploadDate": "2020-07-03 16:25:07", "lastDiallerTimestamp": "2020-07-09 13:59:55", "scheduledCallTimestamp": "2020-07-09 15:59:50", "campaignId": 4, "listId": 4, "isDialling": 0, "leadData": "{\"Email\":\"xxx@xxx.com.au\",\"Address\":\"73 White Road\",\"MQL20\":null,\"HQL2\":null,\"HQL1\":null,\"Industry\":\"\",\"CompanyName\":\"Cofi-Com Trading Pty Limited\",\"HQL3\":null,\"RecordComments1\":null,\"RecordComments2\":null,\"RecordComments3\":null,\"RecordComments4\":null,\"MQL10\":null,\"MQL4\":null,\"MQL14\":null,\"MQL5\":null,\"MQL13\":null,\"MQL6\":null,\"MQL12\":null,\"City\":\"West Ryde\",\"MQL7\":null,\"MQL11\":null,\"MQL18\":null,\"Postcode\":\"2114\",\"MQL1\":null,\"MQL17\":null,\"BasicLead\":null,\"MQL2\":null,\"MQL16\":null,\"CallRecording\":null,\"MQL3\":null,\"MQL15\":null,\"MQL19\":null,\"MQL8\":null,\"MQL9\":null,\"State\":\"\",\"GlobalCompanySize\":null,\"Country\":\"AU\",\"LastName\":\"Black\",\"LocalCompanySize\":\"100 - 249\",\"HQL_Timeframe3\":null,\"HQL_Timeframe2\":null,\"HQL_Timeframe1\":null,\"Authority\":null,\"Content_Syndication\":null,\"Salutation\":\"Mr\",\"JobTitle\":\"Information Technology Head\",\"Filtering3\":null,\"Filtering2\":null,\"Filtering4\":null,\"FirstName\":\"John\",\"Filtering1\":null,\"RH_RID\":null,\"HQL_OpID1\":null,\"HQL_OpID3\":null,\"Meiro_ID\":null,\"HQL_OpID2\":null,\"QCOptIn\":null}", "dialAttempts": 1, "diallerOutcomes": [], "wrapCodeId": 0, "leadInteractions": [{"interactionId": 578, "activities": [642]}], "leadActivities": [{"activityId": 642, "interactions": [578]}]}
df=pd.DataFrame.from_dict(json_in, orient='index')
df_final=pd.DataFrame.from_dict(json.loads(df.loc['leadData',:][0]), orient='index')
#To get transpose of the dataframe - Values in the Column Rather than index
df_final=df_final.T
#To copy a particular column to another dataframe
df_final.loc[:,"campaignTitle"]=df.loc["campaignTitle",:][0]
df_final.to_csv("<output-file.csv>", index=None)
```