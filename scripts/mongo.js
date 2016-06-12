mongoimport --db shadowfax --collection orderData --type csv --headerline --file /home/rohit/Desktop/venturesity/order_data.csv
mongoimport --db shadowfax --collection riderLocation --type csv --headerline --file /home/rohit/Desktop/venturesity/rider_location.csv



db.order_data.find().forEach(function(obj){
	db.order_data.update(obj,{$set:{"actual_time":(Date.parse(obj.delivered_time)-Date.parse(obj.scheduled_time))/1000}})
});



db.order_data.find().forEach(function(obj){
	var min_time_within_cluster=null;
	var min_time_accross_cluster=null;
	var predicted_rider_id;
	db.order_data.update(obj,{$set:{"actual_time":(Date.parse(obj.delivered_time)-Date.parse(obj.scheduled_time))/1000}});
	if(obj.hasOwnProperty('riders_distancemetrix_within_cluster')&&obj.riders_distancemetrix_within_cluster.length>0){
		min_time_within_cluster=obj.riders_distancemetrix_within_cluster[0].duration;
		for(i=0;i<obj.riders_distancemetrix_within_cluster.length;i++){
			if(min_time_within_cluster>obj.riders_distancemetrix_within_cluster[i].duration)
				min_time_within_cluster=obj.riders_distancemetrix_within_cluster[i].duration;
				predicted_rider_id=obj.riders_distancemetrix_within_cluster[i].availabe_rider_id;
			}
		}
	if(!(min_time_within_cluster===null)){
		db.order_data.update(obj,{$set:{"predicted_time_within_cluster":min_time_within_cluster+obj.transit_distancemetrix.duration}});
		db.order_data.update(obj,{$set:{"predicted_rider_id_within_cluster":predicted_rider_id}});
	}
	if(obj.hasOwnProperty('riders_distancemetrix_accross_cluster')&&obj.riders_distancemetrix_accross_cluster.length>0){
		min_time_accross_cluster=obj.riders_distancemetrix_accross_cluster[0].duration;
		for(i=0;i<obj.riders_distancemetrix_accross_cluster.length;i++){
			if(min_time_accross_cluster>obj.riders_distancemetrix_accross_cluster[i].duration)
				min_time_accross_cluster=obj.riders_distancemetrix_accross_cluster[i].duration;
				predicted_rider_id=obj.riders_distancemetrix_accross_cluster[i].availabe_rider_id;
			}
		}
	if(!(min_time_accross_cluster===null)){
		db.order_data.update(obj,{$set:{"predicted_time_accross_cluster":min_time_accross_cluster+obj.transit_distancemetrix.duration}});
		db.order_data.update(obj,{$set:{"predicted_rider_id_accross_cluster":predicted_rider_id}});
	}
});


mongoexport --db shadowfax --collection order_data --query '{"delivered_time":{$ne:null}}' --csv --fields order_id,rider_id,actual_time,predicted_rider_id_within_cluster,predicted_time_within_cluster,predicted_time_accross_cluster,predicted_rider_id_accross_cluster --out /home/rohit/Desktop/venturesity/predicted_order_data.csv;



