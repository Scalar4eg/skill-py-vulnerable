# gcloud upload, make sure to run gcloud init first
HOSTNAME=vulnerable-app1
echo "[SETUP]"
gcloud compute ssh root@$HOSTNAME -- "mkdir app && cd app && python3 -m pip install flask python-dotenv"
echo "[COPY FILES]"
gcloud compute scp \
  ./static \
  ./templates \
  ./*.py \
  ./.env \
  ./run.sh \
  root@$HOSTNAME:~/app --recurse