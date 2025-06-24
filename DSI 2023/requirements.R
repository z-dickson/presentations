
# Specify the URL of a CRAN mirror
cran_mirror <- "https://cran.r-project.org"

# libraries required for the analysis 
install_packages <- c("fect", "dplyr", "kableExtra", "modelsummary", "ggplot2", "grf")

# Install packages from the specified CRAN mirror
install.packages(install_packages, repos = cran_mirror)
