import log_utils
import datetime
import os
from global_defs import *
import pathlib

log = log_utils.logging_init(__file__)

def get_week_product_sn_from_snfile():
	app_path = os.path.dirname(os.path.realpath(__file__))
	log.debug("app_path:%s", app_path)
	snfile_uri = app_path + "/" + FILE_NAME_OF_SN_COUNT_OF_WEEK
	log.debug("snfile_uri:%s", snfile_uri)
	if os.path.exists(snfile_uri) is False:
		snfile = open(snfile_uri, "w+")
		snfile.write("001")
		snfile.flush()
		snfile.close()

	snfile = open(snfile_uri, "r")
	week_product_sn = snfile.read()
	log.debug("week_product_sn:%s", week_product_sn)
	# i_week_product_sn = int(week_product_sn)
	# i_week_product_sn +=2
	# log.debug("week_product_sn in int:%s", str(i_week_product_sn).zfill(3))
	snfile.close()
	return week_product_sn


def increase_week_product_sn():
	app_path = os.path.dirname(os.path.realpath(__file__))
	log.debug("app_path:%s", app_path)
	snfile_uri = app_path + "/" + FILE_NAME_OF_SN_COUNT_OF_WEEK
	log.debug("snfile_uri:%s", snfile_uri)
	if os.path.exists(snfile_uri) is False:
		snfile = open(snfile_uri, "w+")
		snfile.write("001")
		snfile.flush()
		snfile.close()

	snfile = open(snfile_uri, "r")
	week_product_sn = snfile.read()
	log.debug("week_product_sn:%s", week_product_sn)
	i_week_product_sn = int(week_product_sn)
	i_week_product_sn += 1
	log.debug("week_product_sn in int:%s", str(i_week_product_sn).zfill(3))
	snfile.close()
	snfile = open(snfile_uri, "w+")
	snfile.write(str(i_week_product_sn).zfill(3))
	snfile.flush()
	snfile.close()


def reset_week_product_snfile():
	app_path = os.path.dirname(os.path.realpath(__file__))
	log.debug("app_path:%s", app_path)
	snfile_uri = app_path + "/" + FILE_NAME_OF_SN_COUNT_OF_WEEK
	log.debug("snfile_uri:%s", snfile_uri)
	if os.path.exists(snfile_uri) is False:
		snfile = open(snfile_uri, "w+")
		snfile.write("001")
		snfile.flush()
		snfile.close()
	else:
		m_timestamp = pathlib.Path(snfile_uri).stat().st_mtime
		# date_mod = datetime.date(m_timestamp)
		date_mod = datetime.datetime.fromtimestamp(m_timestamp)
		date_mod_year, date_mod_week_num, date_mod_day_of_week = date_mod.isocalendar()
		log.debug("date_mod_week_num = %d", date_mod_week_num)

		date_today = datetime.date.today()
		date_today_year, date_today_week_num, date_today_day_of_week = date_today.isocalendar()
		log.debug("date_today_week_num = %d", date_today_week_num)

		if date_mod_week_num != date_today_week_num:
			log.debug("week already past, need re-count the week_product_sn")
			snfile = open(snfile_uri, "w+")
			snfile.write("001")
			snfile.flush()
			snfile.close()



