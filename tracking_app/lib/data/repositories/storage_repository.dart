import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/data/models/watch_data.dart';


class StorageRepository {
  final _db = FirebaseFirestore.instance;
  Map<String, dynamic> _summary = {};
  Map<String, dynamic> _goal = {};
  List<Map<String, dynamic>> _data = [];

  Map<String, dynamic> get summary => _summary;
  Map<String, dynamic> get goal => _goal;
  List<Map<String, dynamic>> get data => _data;

  Future<bool> saveToDatabase(String userID, String docName, WatchData data) async {
    int? comp;
    bool? track;

    DateTime dayBefore = DateTime.now().subtract(Duration(days:1));
    String previous = '${dayBefore.year}${DateFormat('MMMM').format(dayBefore)}${dayBefore.day}';
    if (await getSummaries(userID, previous)) { 
      print(_summary['snacking']);
      comp = _summary['snacking'] - data.snackingTime; }

    await getGoal(userID);
    if (_goal['currentGoal'] != -1) {
      if (_goal['currentGoal'] >= data.snackingTime) { track = true; }
      else if (_goal['currentGoal'] < data.snackingTime) { track = false; }
    }

    final dailyData = {
      "comments": "",
      "comparison": comp,
      "date": data.date,
      "eating": data.eatingTime,
      "onTrack": track, 
      "snacking": data.snackingTime,
    };
    try {
      await _db.collection("users").doc(userID).collection("summaries").doc(docName).set(dailyData);
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> getSummaries(String userID, String docName) async {
    final dateSummary = _db.collection("users").doc(userID).collection("summaries").doc(docName);
    final DocumentSnapshot doc = await dateSummary.get().catchError((error) { 
      throw error;
    });
    if (doc.exists) {
      _summary = doc.data() as Map<String, dynamic>;
      return true;
    } 
    return false;
  }

    Future<bool> addComment(String comment, String userID, String docName) async {
    final info = _db.collection("users").doc(userID).collection("summaries").doc(docName);
    try {
      await info.update({"comments": comment});
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> getGoal(String userID) async {
    final goalInfo = _db.collection("users").doc(userID);
    final DocumentSnapshot doc = await goalInfo.get().catchError((error) { 
      throw error;
    });
    if (doc.exists) {
      _goal = doc.data() as Map<String, dynamic>;
      return true;
    } 
    return false;
  }

  Future<bool> setGoal(int goal, String userID) async {
    final goalInfo = _db.collection("users").doc(userID);
    try {
      await goalInfo.update({"currentGoal": goal});
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> fetchUserData(String userID) async {
    final userData = _db.collection("users").doc(userID).collection("summaries");
    final QuerySnapshot<Map<String, dynamic>> items = await userData.get().catchError((error) { 
      throw error;
    });
    if (items.size > 0) {
      _data = items.docs.map((item) => item.data()).toList();
      return true;
    } 
    return false;
  }

  void initUser(String userID) async {
    await _db.collection("users").doc(userID).set({"currentGoal": -1});
    await _db.collection("users").doc(userID).collection("summaries").doc("init").set({"status": "User created."});
  }


}


