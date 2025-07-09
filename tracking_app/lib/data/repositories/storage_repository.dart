import 'package:cloud_firestore/cloud_firestore.dart';


class StorageRepository {
  final _db = FirebaseFirestore.instance;
  Map<String, dynamic> _summary = {};
  Map<String, dynamic> _goal = {};
  List<Map<String, dynamic>> _data = [];

  Map<String, dynamic> get summary => _summary;
  Map<String, dynamic> get goal => _goal;
  List<Map<String, dynamic>> get data => _data;

  Future<bool> saveToDatabase(String userID, String docName) async {
    final dailyData = {
      // hard-coded right now, but need to changed the values to data from server
      // get data from WatchData object that's created after fetching data
      "comments": "",
      "comparison": 0,
      "date": "20250705",
      "eating": 20,
      "onTrack": true,
      "snacking": 5,
      // need logic here to populate comparison and onTrack
      // comparison: compare with data from previous day (if any)
      // onTrack: compare with goal that's saved in DB (if any)
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


