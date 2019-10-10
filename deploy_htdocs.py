#!/usr/bin/env python3

import os
import sys
import time

from lib.aws.s3 import S3BucketDeploy
from lib.aws.cloudfront import CloudFrontDistribution


if not os.path.exists(".git/"):
    sys.exit("*** Must be executed from base of the git repository.")



HONK_SOURCE_DIR = "htdocs/"
HONK_S3_BUCKET = "rarepepemuseum.com"
HONK_CLOUDFRONT_DISTRIBUTION = "E33X3LXLI0JEU7"

start_time = time.time()
s3 = S3BucketDeploy(HONK_SOURCE_DIR, HONK_S3_BUCKET)
s3.put_dir()
print("")
cf = CloudFrontDistribution(HONK_CLOUDFRONT_DISTRIBUTION)
cf.invalidate_all()

print("deploy total time: %.4f seconds" % (time.time() - start_time))
