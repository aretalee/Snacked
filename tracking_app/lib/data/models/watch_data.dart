

class WatchData {
  final int snackingTime;
  final int eatingTime;
  final String date;
  final String watchID;

  WatchData({required this.snackingTime, required this.eatingTime, required this.date, required this.watchID});
  int get snack => snackingTime;
  int get eat => eatingTime;
  String get day => date;
  String get id => watchID;

}




