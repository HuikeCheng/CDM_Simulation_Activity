# load packages
 library(ggplot2)

# read data
mydata <- read.csv("mydata.csv")

# education level
ggplot(mydata, aes(education_level)) +
  geom_bar()

# country & age
ggplot(mydata, aes(x=age, color=country)) +
  geom_boxplot()

# gene expression
heatmap(as.matrix(mydata[,3:12]))

# country & gender
ggplot(mydata, aes(x = country, fill = gender)) +
  geom_bar()

# country, gender, height
ggplot(mydata, aes(x=height, color=country)) +
  geom_boxplot() +
  facet_grid(rows = vars(gender))

# country, gender, bmi
ggplot(mydata, aes(x=bmi, color=country)) +
  geom_boxplot() +
  facet_grid(rows = vars(gender))

# case control
model_data <- mydata[,-c(1, 13, 14, 16)]
fit <- glm(status ~ bmi + SNP1 + SNP2 + SNP3 + SNP4 + SNP5, data = model_data, family = 'binomial')
summary(fit)
