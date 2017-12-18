import config
import utils


__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


cfg = config.read()
filter_string = cfg.get("archive","filters")

utils.get_urls_from_filters(filter_string)
