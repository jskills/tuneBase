import logging

# Add after imports, before any other code
logging.getLogger().setLevel(logging.DEBUG)

def run(self):
    logger.debug('Connecting to Strava')
    athlete = self._get_athlete()
    logger.info("Now authenticated for %s %s", athlete.firstname, athlete.lastname)

    # We open the cardioactivities CSV file and start reading through it
    cardio_file = FileUtils.get_cardio_file()
    with cardio_file as csvfile:
        activities = csv.DictReader(csvfile)
        logger.debug('CSV Headers: %s', activities.fieldnames)
        self.distance_mode = DistanceMode.from_csv_header(activities.fieldnames)

        for row in activities:
            logger.debug('Starting to process new row')
            try:
                logger.debug('Row data: %s', dict(row))  # Convert row to dict for better logging
                
                if 'Type' not in row:
                    logger.error('Type field missing from row')
                    logger.debug('Available fields: %s', list(row.keys()))
                    continue

                # Get activity type first since we need it in both branches
                raw_activity_type = str(row['Type'])
                logger.debug('Activity type: %s', raw_activity_type)
                
                # if there is a gpx file listed, find it and upload it
                gpx_file = row['GPX File']
                if ".gpx" in gpx_file:
                    activity_type = RunkeeperToStravaImporter.activity_translator(raw_activity_type)

                    if activity_type is not None:
                        if self.upload_gpx(gpx_file, activity_type, row['Notes']):
                            self.activity_counter += 1
                    else:
                        logger.error('Invalid activity type %s, skipping file %s', raw_activity_type, gpx_file)
                        FileUtils.skip_file(gpx_file, dry_run=self.dry_run)

                # if no gpx file, upload the data from the CSV
                else:
                    self._create_activity_from_csv(raw_activity_type, row)
            except Exception as e:
                logger.error('Error processing row: %s', str(e))
                logger.debug('Row data: %s', row)
                logger.debug('Exception details:', exc_info=True)

        logger.info("Complete! Created %d activities.", self.activity_counter) 