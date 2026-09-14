# firth_check_A.R v1.1 -- R logistf side of the Firth consistency check (driven by tools/firth_check_A.py; 2026-09-13).
# v1.1 (2026-09-14, deviation D-33, registrant decision (A)): each penalized likelihood ratio test now tests only the named coefficient,
#   passing its integer index in the ordered effects to logistftest. v1 passed test = ~ . - term, which tests every other coefficient
#   including the intercept (R df 3 and 6 in run 1). Tolerances, datasets, R control, Python control and the compared quantities are unchanged.
# Usage: Rscript tools/firth_check_A.R <workdir> "<logistf.control(...) expression from contrasts-A.json firth_check.R_control>"
# Writes <workdir>/r_results.csv (dataset, quantity, term, value with 17 significant digits), <workdir>/r_session.txt,
# and exports the bundled datasets (sex2, and endometrial when bundled) to CSV so that firth.py fits the identical data.
# Fence: no number produced here may be cited as evidence that an AI does (or does not) have consciousness, intent, personality, soul, or suffering.
args <- commandArgs(trailingOnly = TRUE)
wd <- args[1]
suppressPackageStartupMessages(library(logistf))
ctl <- eval(parse(text = args[2]))
res <- list()
add <- function(ds, q, term, v) {
  res[[length(res) + 1]] <<- data.frame(dataset = ds, quantity = q, term = term, value = sprintf("%.17g", as.numeric(v)), stringsAsFactors = FALSE)
}
full_loglik <- function(f) {
  ll <- f$loglik
  if (!is.null(names(ll)) && "full" %in% names(ll)) return(unname(ll[["full"]]))
  max(ll)
}
run <- function(ds, fml, dat, terms) {
  f <- logistf(fml, data = dat, control = ctl, pl = FALSE)
  cf <- coef(f)
  for (nm in names(cf)) add(ds, "coef", nm, cf[[nm]])
  add(ds, "loglik_full", "full", full_loglik(f))
  for (tt in terms) {
    j <- match(tt, names(cf))
    if (is.na(j)) stop(paste("term not found among the coefficients:", tt))
    tr <- logistftest(f, test = j, control = ctl)   # v1.1: test only this coefficient (logistf documents integer indexes of the ordered effects); v1 used ~ . - term, which tests all other coefficients including the intercept (deviation D-33)
    ll <- as.numeric(tr$loglik)
    add(ds, "test_loglik_1", tt, ll[1])
    add(ds, "test_loglik_2", tt, ll[2])
    add(ds, "test_stat", tt, 2 * abs(ll[2] - ll[1]))
    add(ds, "test_df", tt, tr$df)
    add(ds, "test_prob", tt, tr$prob)
  }
}
for (nm in c("synth_rising_ptconst", "synth_mid_delta", "synth_floor_sparse")) {
  d <- read.csv(file.path(wd, paste0(nm, ".csv")))
  run(nm, y ~ arm + z + arm:z, d, c("arm:z"))
}
data(sex2, package = "logistf")
write.csv(sex2, file.path(wd, "sex2.csv"), row.names = FALSE)
run("sex2", case ~ age + oc + vic + vicl + vis + dia, sex2, c("age", "oc", "vic", "vicl", "vis", "dia"))
has_endo <- tryCatch({ data(endometrial, package = "logistf"); exists("endometrial") }, warning = function(w) FALSE, error = function(e) FALSE)
if (isTRUE(has_endo)) {
  write.csv(endometrial, file.path(wd, "endometrial.csv"), row.names = FALSE)
  run("endometrial", HG ~ NV + PI + EH, endometrial, c("NV", "PI", "EH"))
}
out <- do.call(rbind, res)
write.csv(out, file.path(wd, "r_results.csv"), row.names = FALSE)
writeLines(c(R.version.string, paste("logistf", as.character(packageVersion("logistf"))), paste("endometrial bundled:", isTRUE(has_endo))), file.path(wd, "r_session.txt"))
