from Parse import deduped_data as dataset
from haversine import haversine, Unit
# Pickup lat long extraction
dataset['pickup_latitude'] = dataset['latitude'].astype(float)
dataset['pickup_longitude'] = dataset['longitude'].astype(float)

dakshindari= (22.610619, 88.409662)
sector_5=(22.597692, 88.432226)
victoria_memorial=(22.552652, 88.352503)
howrah=(22.583474, 88.342969)
airport=(22.642434, 88.439351)

def calculate_distance(coords,lat, lon):
    point_coords = (lat, lon)
    return haversine(coords, point_coords, unit=Unit.KILOMETERS)

dataset['aerial_dist_dakshindari'] = dataset.apply(
    lambda row: calculate_distance(dakshindari,row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_sector_V'] = dataset.apply(
    lambda row: calculate_distance(sector_5,row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_rabindrasadan_metro'] = dataset.apply(
    lambda row: calculate_distance(victoria_memorial,row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_howrah'] = dataset.apply(
    lambda row: calculate_distance(howrah,row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_airport'] = dataset.apply(
    lambda row: calculate_distance(airport,row['pickup_latitude'], row['pickup_longitude']), axis=1
)


dataset_rabindrasadan=dataset[dataset['aerial_dist_rabindrasadan_metro']<2]
dataset_airport=dataset[dataset['aerial_dist_airport']<2]
dataset_dakshindari=dataset[dataset['aerial_dist_dakshindari']<2]
dataset_howrah=dataset[dataset['aerial_dist_howrah']<2]
dataset_sectorV=dataset[dataset['aerial_dist_sector_V']<2]



print("processed")
