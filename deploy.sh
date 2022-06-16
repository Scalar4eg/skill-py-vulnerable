# gcloud upload, make sure to run gcloud init first
HOSTNAME=vulnerable-app1
gcloud compute scp \
  ./static \
  ./templates \
  ./*.py \
  ./.env \
  $HOSTNAME:~/app --recurse