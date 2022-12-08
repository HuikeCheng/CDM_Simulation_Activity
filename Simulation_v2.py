########## Import packages #############
from faker import Faker
import random
import numpy as np
from numpy.random import normal
import pandas as pd

########## create object for making fake data ###########
fake = Faker()

######### set seed ###########
random.seed(0) # not sure if this is how to do it

########## sample_id (any reference of your choice) if in 8-digit barcode ##########
sample_ID = np.random.randint(10000, 99999, size=500)
sample_ID = sample_ID.tolist()
for i in range(500):
    sample_ID[i] = '000' + str(sample_ID[i])

mydata = pd.DataFrame(sample_ID, columns=['sid'])

############# education level #############
els = ['Primary', 'Secondary', 'Bachelor', 'Masters', 'PhD']
el = np.random.choice(els, 500, p = [0.1, 0.3, 0.3, 0.2, 0.1])
# add to dataset
mydata = pd.concat([mydata, el], axis=1)

############ 10 gene_expression values ranging from ###########
a = [
    {"gene1": np.random.uniform(-3 ,3),
     "gene2": np.random.uniform(-3 ,3),
     "gene3": np.random.uniform(-3 ,3),
     "gene4": np.random.uniform(-3 ,3),
     "gene5": np.random.uniform(-3 ,3),
     "gene6": np.random.uniform(-3 ,3),
     "gene7": np.random.uniform(-3 ,3),
     "gene8": np.random.uniform(-3 ,3),
     "gene9": np.random.uniform(-3 ,3),
     "gene10": np.random.uniform(-3 ,3)}
    for x in range(500)]

df = pd.DataFrame(a)

mydata = pd.concat([mydata, df], axis=1)

############ country & city ##########
country_city = pd.read_csv('country_city.csv')

def sample_country_city(country_city, n=500):
    cc_list=[]
    for i in range(n):
        data = pd.DataFrame.sample(country_city).values[0]
        cc_list.append(data)
    return cc_list

country_city_list = sample_country_city(country_city)

cc_arr = np.array(country_city_list)
cc_df = pd.DataFrame(cc_arr, columns = ["country", "city"])

mydata = pd.concat([mydata, cc_df], axis=1)

############# gender ##############
country_info = pd.read_csv('country_info.csv')

gender_list = []
for i in mydata['country']:
    prop_f = float(country_info['prop_f'].loc[country_info['country'] == i])
    prop_m = float(country_info['prop_m'].loc[country_info['country'] == i])
    gender = np.random.choice([0, 1], 1, p=[prop_f, prop_m])
    gender_list.append(gender)

gen_arr = np.array(gender_list)
gen_df = pd.DataFrame(gen_arr, columns = ["gender"])

mydata = pd.concat([mydata, gen_df], axis=1)

############ name (First and Last) ############
def gen_name(x):
    if x == "Female":
        return fake.name_female()
    else: 
        return fake.name_male()

name = mydata["gender"].apply(gen_name)

mydata["name"] = name

######### age ############
age_list = []
for i in mydata['country']:
    age_sta = int(random.randint(0,2))
    med_age = int(country_info['median age'][country_info['country'] == i])
    if age_sta == 0:
        age = random.sample(range(18, med_age), 1)
    else:
        age = random.sample(range(med_age, 65), 1)
    age_list.append(age)

age_arr = np.array(age_list)
age_df = pd.DataFrame(age_arr, columns = ["age"])

mydata = pd.concat([mydata, age_df], axis=1)

########### bmi ###########
def gen_bmi(x):
    if x == "Female":
        return float(normal(loc=22.5, scale=5, size=1))
    else: 
        return float(normal(loc=26.5, scale=6, size=1))

bmi = mydata["gender"].apply(gen_bmi)

mydata["bmi"] = bmi

########## height ###########
def gen_height(x):
    if x == "Female":
        return float(normal(loc=164.4, scale=5.59, size=1))
    else: 
        return float(normal(loc=178.2, scale=6.35, size=1))

height = mydata["gender"].apply(gen_height)

mydata["height"] = height




######## 5 SNP values (0,1,2) ##########
# rs2231142: MAF=0.10
# rs16890979: MAF=0.30
# rs2910164: MAF=0.31
# rs6922269: MAF=0.27
# rs17228212: MAF=0.26
def calc_hwe(maf):
    p_0 = round((1-maf)*(1-maf), 2)
    p_1 = round(maf*(1-maf), 2)
    p_2 = round(maf*maf, 2)
    p = [p_0, p_1, p_2]
    return p

def gen_SNP(x):
    return random.choices([0,1,2], calc_hwe(x), k=500)

MAFs = pd.DataFrame([0.1, 0.3, 0.31, 0.27, 0.26], columns = ["MAF"])
SNPs = MAFs["MAF"].apply(gen_SNP)

df_SNP = pd.DataFrame(list(SNPs)).T
df_SNP.columns = ["SNP1", "SNP2", "SNP3", "SNP4", "SNP5"]

mydata = pd.concat([mydata, df_SNP], axis=1)

############### case_control status defined as a function of some of your other variables ##############
# logit_p = b0 + b1*var1
# p = 1/(1+exp(-(logit_p)))
# y ~ binomial(1, p)
logit_p = 0.2*mydata["bmi"] + 0.3*mydata["SNP2"] + 1.2*mydata["SNP5"]
p = 1/(1 + np.exp(-1*logit_p))
status = np.random.binomial(1, p, size = 500)

mydata["status"] = status

########## final dataset ###########
mydata.head()

############# write to csv file #############
mydata.to_csv('mydata.csv', index = False)