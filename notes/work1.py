import json
from types import CodeType
import pandas as pd
import numpy as np

with open(
    "/gpfs/fs0/scratch/a/archer/beapen/home/scratch/fhiry/data/fhir/Aaafhir.json", "r"
) as f:
    json_in = f.read()

json_in = json.loads(json_in)
# df=pd.DataFrame.from_dict(json_in, orient='index')
# print(df)
# df_final = pd.DataFrame.from_dict(json.loads(
#     df.loc['entry', :][0]), orient='index')
# print(df_final)

#  This works
df = pd.json_normalize(json_in["entry"])
# df.fillna('', inplace=True)
# df = df.applymap(str)
# print(df.info())
# print(df['resource.resourceType'], df['resource.id'])
# print(df['resource.class.system'].notna(), df['resource.class.code'].notna())
# print(df['resource.resourceType'])


patient = df[(df["resource.resourceType"] == "Patient")].iloc[0]["resource.id"]
df["patientId"] = patient


def process_list(mylist):
    mycodes = []
    if isinstance(mylist, list):
        for entry in mylist:
            if "code" in entry:
                mycodes.append(entry["code"])
            else:
                mycodes.append(entry["display"])
    return mycodes


# iterating the columns


# Delete unwanted cols
del df["resource.text.div"]

# Add patient details to all rows
# df['resource.gender'].fillna(df['resource.gender'].mode()[0], inplace=True)
# df['resource.birthDate'].fillna(
#     df['resource.birthDate'].mode()[0], inplace=True)

for col in df.columns:
    if "coding" in col:
        codes = df.apply(lambda x: process_list(x[col]), axis=1)
        df = pd.concat([df, codes.to_frame(name=col + "codes")], 1)
        del df[col]
    if "display" in col:
        codes = df.apply(lambda x: process_list(x[col]), axis=1)
        df = pd.concat([df, codes.to_frame(name=col + "display")], 1)
        del df[col]

# for col in df.columns:
#     try:
#         df[col] = df[col].apply(lambda y: np.nan if len(y) == 0 else y)
#     except:
#         pass

# codes = df.apply(lambda x: process_list(x['resource.code.coding']), axis=1)
# df = pd.concat([df, codes.to_frame(name='resource.code.coding.codes')], 1)
# codes = df.apply(lambda x: process_list(x['resource.class.code']), axis=1)
# df = pd.concat([df, codes.to_frame(name='resource.class.code.codes')], 1)

# Flatten
# del df['fullUrl']
# df2=None
# for index, _ in df.iterrows():
#     if index > 0:
#         df2 = df.head(1).combine_first(df.loc[[index]])
#         print(df2.info())
#         if index > 30:
#             break
print(df.head(5))
print(df["patientId"])
# df3 = df2.tail(1)
# print(df3.head().values)

# print(df3.info())

# def objects_to_resources(df):
#     return pd.Series(
#         get_resource(row) for index, row in df.iterrows()
#     )


# def get_resource(row):
#     if row['resource.resourceType'] == 'Observation':
#         print(str(row))
#         return Observation(str(row))
#     return row


# df['resources'] = objects_to_resources(df)
# print(df['resources'])

# df.apply(
#     lambda row:
#         print(row) if row['resource.resourceType'] == 'Observation' else print (""), axis=1
# )

# iterating the columns
# for col in df.columns:
#     print(col)

# csv
# print(df.to_csv(index=True))

# df2 = pd.read_json(
#     '/gpfs/fs0/scratch/a/archer/beapen/home/scratch/fhiry/data/fhir/Aaafhir.json')
# print(df2)
