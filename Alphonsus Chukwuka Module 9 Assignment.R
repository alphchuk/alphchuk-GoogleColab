#Name : Alphonsus Chukwuka
#Student ID : A00228932
#Applied Activity 9

library(ggplot2)

##Question 1


'''
#1a
#Null and alternate hypotheses
H0: The acceptance rate for males and females is the same in the four college programs

HA: The acceptance rate for males and females is differente in the four college programs 
'''

#1b

#Enter the data
#Order of programs: "Business", "Performing Arts", "Computer Tech", "Health Sciences"

male<- c(315,225,300,360)
female<-c(190,160,210,240)

#Combine the two groups into a single data set

coll_acceptance<- rbind(male, female) #bind by rows

#insert column names
colnames(coll_acceptance)<-c("Business", "Performing Arts", "Computer Tech", "Health Sciences")

coll_acceptance

#Performimg chi-square test for homogeneity

alpha= 0.05

row.total<-apply(coll_acceptance, 1, sum) #row total
column.total<-apply(coll_acceptance, 2, sum) #column total
total<-sum(coll_acceptance) #grand total

expected<-outer(row.total, column.total)/total #expected 
#chi-square test
(chi2.colaccept<-sum((coll_acceptance-expected)^2/expected)) #1.8718

#BUILT IN FUNCTION
coll_axpt = chisq.test(coll_acceptance) #confirms above

'''
Pearsons Chi-squared test

data:  coll_acceptance
X-squared = 1.8718, df = 3, p-value = 0.5994
'''


#Using critical values
qchisq(0.05, df=(dim(coll_acceptance)[1]-1)*(dim(coll_acceptance)[2]-1), lower.tail=FALSE) #7.8147

#Conclusion
#X^2 = 1.8718 < 7.8147 = X^2*

#Fail to reject the null, there is no significant difference in the acceptance rate for males and females in the four college programs

#1c

#Get the residuals from the test
(residuals.collaccpt<-coll_axpt$residuals)
'''
 Business Performing Arts Computer Tech Health Sciences
male    0.6893820      -0.3947710    -0.3429972               0
female -0.8443171       0.4834938     0.4200840               0
'''

#1d
#Association Plot 
assocplot(coll_acceptance, xlab="Courses", ylab="Colours",
          main="Association Plot for College Acceptance Rate by Courses")

#The tallest bar corresponds to Female acceptance into Business Course. This means that this is the most unusual residual. 
#The tallest red bar is for Female acceptance into Business Course which means it is the largest negative residual.
#The tallest black bar is for Male acceptance into Business Course which means it is the largest positive residual.
#The widest bar is for Male acceptance into Business Course. This means that is where we expected the highest count of Smarties. 
#The most narrow bar is Female acceptance into Performing Arts Course. This means that is where we expected the lowest count of Smarties.


##Question 2

#Read in the  data 
course<-read.csv(file.choose(), header=TRUE, fileEncoding="UTF-8-BOM")
#create subsets
BAPG<-subset(course, Program=="BAPG")
CAGC<-subset(course, Program=="CAGC")
HAGC<-subset(course, Program=="HAGC")

library(dplyr)
BAPG.50<-sample_n(BAPG, 50)
CAGC.50<-sample_n(CAGC, 50)
HAGC.50<-sample_n(HAGC, 50)
full.50<-rbind(BAPG.50, CAGC.50, HAGC.50)

'''
Add a categorical variable to the data set with two categories:

Above if the hours studied are greater than 3.13 hours
Below if the hours studied are less than or equal to 3.13 hours
'''
full.50$HoursCategory<-ifelse(full.50$Study>3.13, "Above", "Below")

#summarize the days that are "Above" and "Below" by program category using a table.

observed.hours<-table(full.50$HoursCategory, full.50$Program)
observed.hours


'''

#Null and alternate hypotheses
H0: The distribution of above and below days is independent of program

HA: The distribution of above and below days is not independent of program 
'''

#Perform chi suare test using built in function
chisq.test(observed.hours) 

'''
Pearsons Chi-squared test

data:  observed.hours
X-squared = 0.3744, df = 2, p-value = 0.8293
'''

#Using critical values
qchisq(0.05, df=(dim(observed.hours)[1]-1)*(dim(observed.hours)[2]-1), lower.tail=FALSE) #5.9915

#Conclusion
#X^2 = 0.3744 < 5.9915 = X^2*
##Fail to reject the null, there is significant evidence that the distribution of above and below days is independent of program of study
