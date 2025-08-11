

class WatchData {
  final int snackingTime;
  final int eatingTime;
  final String date;
  final String watchID;

  WatchData({required this.snackingTime, required this.eatingTime, required this.date, required this.watchID});

  // factory WatchData.fromJson(Map<String, dynamic> json) {
  //   return WatchData(
  //     snackingTime: json["duration"] as int,
  //     eatingTime: json["duration"] as int,
  //     date: json["date"] as String,
  //     watchID: json["watchID"] as String,
  //   );
  // }

  int get snack => snackingTime;
  int get eat => eatingTime;
  String get day => date;
  String get id => watchID;

}




