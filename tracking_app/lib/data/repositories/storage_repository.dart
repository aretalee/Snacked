import 'package:cloud_firestore/cloud_firestore.dart';


class StorageRepository {
  final _db = FirebaseFirestore.instance;
  String _error = '';
  Map<String, dynamic> _contents = {};

  Map<String, dynamic> get contents => _contents;
  String get error => _error;

  Future<bool> getDocument(String docName) async {
    final dateSummary = _db.collection("summaries").doc(docName);
    print('DateSummary path: ${dateSummary.path}');
    final DocumentSnapshot doc = await dateSummary.get().catchError((error) { print('Error: ${error}'); });
    if (doc.exists) {
      _contents = doc.data() as Map<String, dynamic>;
      return true;
    } 
    return false;
  }

}


