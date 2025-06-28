import 'package:cloud_firestore/cloud_firestore.dart';


class StorageRepository {
  final _db = FirebaseFirestore.instance;
  Map<String, dynamic> _contents = {};

  Map<String, dynamic> get contents => _contents;

  Future<bool> getDocument(String docName) async {
    final dateSummary = _db.collection("summaries").doc(docName);
    print('DateSummary path: ${dateSummary.path}');
    final DocumentSnapshot doc = await dateSummary.get().catchError((error) { 
      print('Error: $error}'); 
      throw error;
    });
    if (doc.exists) {
      _contents = doc.data() as Map<String, dynamic>;
      return true;
    } 
    return false;
  }

}


