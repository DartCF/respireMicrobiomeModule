library(readxl)
library(dplyr)
library(readr)
library(janitor)

sam_meta <- read_excel("/Users/f006p17/Downloads/sam_metadata.xlsx", sheet = 'NCBI Studies (2)') %>%
  clean_names()

sam_meta_subset <- sam_meta %>%
  select(dataset_link, organism, study_id = uid, condition) %>%
  mutate(study_id = as.integer(study_id))

sourced_metadata <- read_csv("/Users/f006p17/Downloads/all_microbiome_study_metadata.csv")

sourced_clean <- sourced_metadata %>%
  select(-c(host, bio_sample_model)) %>%
  relocate(data_type, method, .after = last_col())

full <- sam_meta_subset %>%
  left_join(sourced_clean, by = "study_id")

write_csv(full, "/Users/f006p17/Desktop/respire_microbiome_metadata.csv")
