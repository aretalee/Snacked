import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;

import 'package:Snacked/data/models/watch_data.dart';


class FetchService{
  final _supabase = Supabase.instance.client;
  late WatchData fetchedInfo;

  WatchData get fetched => fetchedInfo;

  Future<bool> fetchData() async {
    DateTime summaryDate = DateTime.now().subtract(Duration(days:1));
    String formattedDate = '${summaryDate.year}${DateFormat('MM').format(summaryDate)}${summaryDate.day}';
    final data = await _supabase.from('snackingdata').select('date, watchid').eq('date', formattedDate); 
    // depends on date format that's saved from watch

    final eatDuration = await _supabase.from('snackingdata').select('duration').eq('activitytype', 'Eating').eq('date', formattedDate);

    final snackDuration = await _supabase.from('snackingdata').select('duration').eq('activitytype', 'Snacking').eq('date', formattedDate);
    // see if sum can be supported later

    if (data.isEmpty || eatDuration.isEmpty || snackDuration.isEmpty) { return false; }

    final date = data[0]['date'] as String;
    final watchID = data[0]['watchid'] as String;
    final eating = eatDuration[0]['duration'] as int;
    final snack = snackDuration[0]['duration'] as int;
    
    fetchedInfo = WatchData(snackingTime: snack, eatingTime: eating, date: date, watchID: watchID);
    return true;

  }

  Future<void> callFlow() async {
    final url = Uri.parse('https://prod-55.westeurope.logic.azure.com:443/workflows/7ba510c391d04806867c531edce688aa/triggers/manual/paths/invoke?api-version=2016-06-01');

    var response = await http.post(url);
    if (response.statusCode == 200) { print('Called successfully'); }
    else { print('Call failed'); }

  }

}





