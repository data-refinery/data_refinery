options(warn=2)
options(repos=structure(c(CRAN="https://cloud.r-project.org")))
options(Ncpus=parallel::detectCores())

# Helper function that installs a list of packages using the input URLs
install_with_url <- function(urls) {
  pkg_ids <- devtools::install_url(urls)
  if(any(is.na(pkg_ids))) {
    pkg_fails <- paste(urls[is.na(pkg_ids)], collapse = "; ")
    stop(paste("Failed to install package(s):", pkg_fails ))
  }
  return(pkg_ids)
}

bioc_pkgs <- c(
  'https://bioconductor.org/packages/3.11/bioc/src/contrib/preprocessCore_1.50.0.tar.gz'
)
install_with_url(bioc_pkgs)

# Load these libraries because apparently just installing them isn't
# enough to verify that they have complementary versions.
library("optparse")
library(data.table)
library("preprocessCore")
