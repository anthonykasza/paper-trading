echo "removing old data";
rm data.pkl;

echo "going the distance...";
python distances.py;

echo "going the distance... a second time";
python distances.py;

echo "saving global png";
python global_dist.py;

echo "saving pairwise png";
python pairwise_dist.py;

echo "saving clsters png";
python price_action_clusters.py > clusters;
python subplot_clusters.py;

echo "tidying up";
if [ ! -d "pngs/" ]; then
  mkdir pngs/;
fi
mv *.png pngs/;
