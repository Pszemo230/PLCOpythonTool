SELECT
  age,
  dx_psa,
  pros_gleason,
--  bmi_curr,
  pros_exitage,
  weight_f,
  height_f,
  cig_years,
  numbiopp,
  curative_hormp,
  curative_othp,
  curative_prostp,
  curative_radp
FROM
  prostate_screening.prostate_overall
WHERE dx_psa > 0.0 AND
      (pros_gleason NOT IN (0.0, 99.0))
