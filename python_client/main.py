import pyrefinebio

print(pyrefinebio.Sample.get("GSM824740").organism.taxonomy_id)

samples = pyrefinebio.Sample.search(is_processed=True, specimen_part="soft-tissue sarcoma")

for sample in samples:
    print(sample.id)