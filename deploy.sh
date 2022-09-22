# gcloud upload, make sure to run gcloud init first
HOSTNAME=vulnerable-app2
echo "[SETUP]"
gcloud compute ssh root@$HOSTNAME --zone=us-central1-a  -- "mkdir app && cd app && python3 -m pip install flask python-dotenv"
echo "[COPY FILES]"
gcloud compute scp \
  ./static \
  ./templates \
  ./*.py \
  ./.env \
  ./run.sh \
  root@$HOSTNAME:~/app --zone=us-central1-a  --recurse