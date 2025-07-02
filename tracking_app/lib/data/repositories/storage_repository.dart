import 'package:cloud_firestore/cloud_firestore.dart';


class StorageRepository {
  final _db = FirebaseFirestore.instance;
  Map<String, dynamic> _summary = {};
  Map<String, dynamic> _goal = {};
  Map<String, dynamic> _data = {};

  Map<String, dynamic> get summary => _summary;
  Map<String, dynamic> get goal => _goal;
  Map<String, dynamic> get data => _data;

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
    final goalInfo = _db.collection("users").doc(userID).collection("summaries").doc(docName);
    try {
      await goalInfo.update({"comments": comment});
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> getGoal(String userID) async {
    final goalInfo = _db.collection("users").doc(userID).collection("currentGoal").doc("goal");
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
    final goalInfo = _db.collection("users").doc(userID).collection("currentGoal").doc("goal");
    try {
      await goalInfo.update({"targetTime": goal});
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> fetchUserData(String userID) async {
    final userData = _db.collection("users").doc(userID);
    final DocumentSnapshot doc = await userData.get().catchError((error) { 
      throw error;
    });
    if (doc.exists) {
      _data = doc.data() as Map<String, dynamic>;
      return true;
    } 
    return false;
  }

}


