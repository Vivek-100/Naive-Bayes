from itertools import product
from itertools import combinations
import itertools 
import sys
import copy
import operator
import functools

def inference(dictionary):

    number_of_patients=int(dictionary['Number_of_Patients'][0])
    counter=0
    true_false_counter=0
    while(number_of_patients > 0):
        number_of_disease=int(dictionary['Number_of_Diseases'][0])
        true_false_counter = int(counter) * int(number_of_disease)
        post_probability={}
        min_max={}
        undetermined_values={}
        final_inference = "Patient-"+str(counter+1)+":\n"

        for i,disease_name in enumerate(dictionary['Disease_Name']):
            true_false_counter_inloop = int(int(true_false_counter)+int(i))
            PD=dictionary['Prior_true_value'][i]
            PND=dictionary['Prior_false_value'][i]
            PT=[]
            PF=[]
            PU={}
            undefined_counter=0
            for j,symptoms in enumerate(dictionary['Symptoms'][i]):
                Status_of_Findings = dictionary['Status_of_Findings'][true_false_counter_inloop][j]
                if(Status_of_Findings == 'T'):
                    PT.append(dictionary['Symptoms_true_value'][i][j])
                    PF.append(dictionary['Symptoms_false_value'][i][j])
                if(Status_of_Findings == 'F'):
                    PT.append(1-dictionary['Symptoms_true_value'][i][j])
                    PF.append(1-dictionary['Symptoms_false_value'][i][j])
                if(Status_of_Findings == 'U'):
                    key = disease_name
                    PU.setdefault(key, [])
                    PU[key].append(symptoms)
                    undefined_counter=undefined_counter+1
            
            PTV=functools.reduce(operator.mul, PT, 1)
            PFV=functools.reduce(operator.mul, PF, 1)
            total=(PD*PTV) + (PND*PFV)
            Final_probability = round(float((PD*PTV)/((PD*PTV) + (PND*PFV))),4)
            post_probability[disease_name]=str(format(Final_probability, '.4f'))

            status_counter=0
            combination_table = list(itertools.product([False, True], repeat=undefined_counter))
            status_of_findings=list(dictionary['Status_of_Findings'][true_false_counter_inloop])
            combination_findings=[]
            temp1_finding=[]
            temp2_finding=[]
            for m, status_finding in enumerate(dictionary['Status_of_Findings'][true_false_counter_inloop]):
                if(status_finding=='T' or status_finding=='F'):
                    if not combination_findings:
                        combination_findings.append([status_finding])
                    else:
                        for items in combination_findings:
                            items.extend(status_finding)
                elif(status_finding=='U'):
                    if not combination_findings:
                        temp1_finding.extend('T')
                        temp2_finding.extend('F')
                        temp1_combination=copy.copy(temp1_finding)
                        temp2_combination=copy.copy(temp2_finding)
                        combination_findings.append(temp1_combination)
                        combination_findings.append(temp2_combination)
                        del temp1_finding[:]
                        del temp2_finding[:]
                    else:
                        temp_combination=copy.copy(combination_findings)
                        del combination_findings[:]
                        for items in temp_combination:
                            temp1_finding.extend(items)
                            temp1_finding.extend('T')
                            temp2_finding.extend(items)
                            temp2_finding.extend('F')
                    
                            temp1_combination=copy.copy(temp1_finding)
                            temp2_combination=copy.copy(temp2_finding)
                            combination_findings.append(temp1_combination)
                            combination_findings.append(temp2_combination)
                            del temp1_finding[:]
                            del temp2_finding[:]

            min_value=''
            max_value=''
            PD=dictionary['Prior_true_value'][i]
            PND=dictionary['Prior_false_value'][i]
            
            for Status_values in combination_findings:
                PT=[]
                PF=[]
                PU={}
                for j,symptoms in enumerate(dictionary['Symptoms'][i]):
                    Status_of_Findings = Status_values[j]
                    if(Status_of_Findings == 'T'):
                        PT.append(dictionary['Symptoms_true_value'][i][j])
                        PF.append(dictionary['Symptoms_false_value'][i][j])
                    if(Status_of_Findings == 'F'):
                        PT.append(1-dictionary['Symptoms_true_value'][i][j])
                        PF.append(1-dictionary['Symptoms_false_value'][i][j])
                
                PTV=functools.reduce(operator.mul, PT, 1)
                PFV=functools.reduce(operator.mul, PF, 1)
                total=(PD*PTV) + (PND*PFV)
                max_min_probability = round(float((PD*PTV)/((PD*PTV) + (PND*PFV))),4)
                if(min_value=="" and max_value==""):
                    min_value=str(format(max_min_probability, '.4f'))
                    max_value=str(format(max_min_probability, '.4f'))
                else:
                    if(float(max_min_probability) < float(min_value)):
                        min_value=str(format(max_min_probability, '.4f'))
                    elif(float(max_min_probability) > float(max_value)):
                        max_value=str(format(max_min_probability, '.4f'))

            key = disease_name
            min_max.setdefault(key, [])
            min_max[key].append(min_value)
            min_max[key].append(max_value)

            index_dict={}
            key1 = "symptoms"
            key2 = "index"
            index_dict.setdefault(key1, [])
            index_dict.setdefault(key2, [])
            for j,symptoms in enumerate(dictionary['Symptoms'][i]):
                Status_of_Findings = dictionary['Status_of_Findings'][true_false_counter_inloop][j]
                if(Status_of_Findings == 'U'):
                    index_dict[key1].append(symptoms)
                    index_dict[key2].append(j)
            
            Status_Value = dictionary['Status_of_Findings'][true_false_counter_inloop]
            comb_values={}
            key1 = "symptoms"
            key2 = "change"
            key3 = "list"
            comb_values.setdefault(key1, [])
            comb_values.setdefault(key2, [])
            comb_values.setdefault(key3, [])
            temp1_values=[]
            temp2_values=[]
            for index,index_value in enumerate(index_dict["index"]):
                temp1_values = copy.copy(Status_Value)
                temp2_values = copy.copy(Status_Value)
                temp1_values[index_value]='T'
                comb_values[key1].append(index_dict["symptoms"][index])
                comb_values[key2].append('T')
                comb_values[key3].append(temp1_values)
                temp2_values[index_value]='F'
                comb_values[key1].append(index_dict["symptoms"][index])
                comb_values[key2].append('F')
                comb_values[key3].append(temp2_values)

            max_change=0
            min_change=0
            min_symtom=""
            max_symtom=""
            min_value=""
            max_value=""
            percentage_change=0
            for index,comb_value in enumerate(comb_values["list"]):
                PT=[]
                PF=[]
                PU={}
                for j,symptoms in enumerate(dictionary['Symptoms'][i]):
                    Status_of_Findings = comb_value[j]
                    if(Status_of_Findings == 'T'):
                        PT.append(dictionary['Symptoms_true_value'][i][j])
                        PF.append(dictionary['Symptoms_false_value'][i][j])
                    if(Status_of_Findings == 'F'):
                        PT.append(1-dictionary['Symptoms_true_value'][i][j])
                        PF.append(1-dictionary['Symptoms_false_value'][i][j])
                
                PTV=functools.reduce(operator.mul, PT, 1)
                PFV=functools.reduce(operator.mul, PF, 1)
                total=(PD*PTV) + (PND*PFV)
                changed_probability = round(float((PD*PTV)/((PD*PTV) + (PND*PFV))),4)
                symptom=comb_values["symptoms"][index]
                change=comb_values["change"][index]
                if(float(Final_probability) > float(changed_probability)):
                    percentage_change=((Final_probability - changed_probability)/Final_probability) * 100
                    if(min_change==0):
                        min_change=percentage_change
                        min_symtom=symptom
                        min_value=change
                    elif(percentage_change > min_change):
                        min_change=percentage_change
                        min_symtom=symptom
                        min_value=change
                    elif(percentage_change == min_change):
                        if(min(min_symtom,symptom) == symptom):
                            min_change=percentage_change
                            min_symtom=symptom
                            min_value=change
                elif(float(Final_probability) < float(changed_probability)):
                    percentage_change=((changed_probability - Final_probability)/Final_probability) * 100
                    if(max_change==0):
                        max_change=percentage_change
                        max_symtom=symptom
                        max_value=change
                    elif(percentage_change > max_change):
                        max_change=percentage_change
                        max_symtom=symptom
                        max_value=change
                    elif(percentage_change == max_change):
                        if(min(max_symtom,symptom) == symptom):
                            max_change=percentage_change
                            max_symtom=symptom
                            max_value=change
            
            if(max_symtom==""):
                max_symtom='none'
            if(max_value==""):
                max_value='N'
            if(min_symtom==""):
                min_symtom='none'
            if(min_value==""):
                min_value='N'           
            key = disease_name
            undetermined_values.setdefault(key, [])
            undetermined_values[key].append(max_symtom)
            undetermined_values[key].append(max_value)
            undetermined_values[key].append(min_symtom)
            undetermined_values[key].append(min_value)

        final_inference=final_inference+str(post_probability)+"\n"+str(min_max)+"\n"+str(undetermined_values)
        """write result on the file"""
        file = open(outputFileName, "a+")
        result_str=str(final_inference)
        file.write(result_str+"\n")
        number_of_patients = number_of_patients-1
        counter=counter+1;
    file.close()


""" READ THE INPUT FILE """

inputFile = open(sys.argv[2])
inputFileName=sys.argv[2]
#inputFile = open(r"sample_input.txt",'r')
#inputFileName = "$LIB/home/etc/four/five/sample_input.txt"
MiddleFileName = inputFileName.split('/')
outputFileName = MiddleFileName[5].split('.')
outputFileName=outputFileName[0] + "_inference.txt"
detail={}
line_number=0
number_of_diseases=0
number_of_patients=0
number_of_detail_diseases = 0
for line in inputFile:
    line_number=line_number+1
    if line_number==1:
        spl = line.strip().split(' ')
        number_of_diseases=int(spl[0])
        key = "Number_of_Diseases"
        detail.setdefault(key, [])
        detail[key].append(number_of_diseases)
        number_of_patients=int(spl[1])
        key = "Number_of_Patients"
        detail.setdefault(key, [])
        detail[key].append(number_of_patients)
        number_of_detail_diseases = 4 * number_of_diseases
        file = open(outputFileName, "w")
        file.close()
    elif line_number <= (number_of_detail_diseases+1):
        if line_number % 4 ==2:
            spl = line.strip().split(' ')
            name_of_disease=spl[0]
            key = "Disease_Name"
            detail.setdefault(key, [])
            detail[key].append(name_of_disease)
            number_of_symptoms=int(spl[1])
            key = "Number_of_symptoms"
            detail.setdefault(key, [])
            detail[key].append(number_of_symptoms)
            PD=round(float(spl[2]),4)
            key = "Prior_true_value"
            detail.setdefault(key, [])
            detail[key].append(PD)
            PND=round(float(1-PD),4)
            key = "Prior_false_value"
            detail.setdefault(key, [])
            detail[key].append(PND)
        elif line_number % 4 ==3:
            symptoms = eval(line)
            key = "Symptoms"
            detail.setdefault(key, [])
            detail[key].append(symptoms)
        elif line_number % 4 ==0:
            true_symptoms = eval(line)
            key = "Symptoms_true_value"
            detail.setdefault(key, [])
            detail[key].append(true_symptoms)
        elif line_number % 4 ==1:
            false_symptoms = eval(line)
            key = "Symptoms_false_value"
            detail.setdefault(key, [])
            detail[key].append(false_symptoms)
    elif line_number > number_of_detail_diseases+1: 
            status_of_findings = eval(line)
            key = "Status_of_Findings"
            detail.setdefault(key, [])
            detail[key].append(status_of_findings)

inference(detail)
inputFile.close()  
