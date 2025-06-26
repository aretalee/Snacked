import 'package:cloud_firestore/cloud_firestore.dart';


class StorageRepository {
  final _db = FirebaseFirestore.instance;
  String _error = '';
  Map<String, dynamic> _contents = {};

  Map<String, dynamic> get contents => _contents;
  String get error => _error;


  // bool? getDocument(String docName) {
  //   final dateSummary = _db.collection("summaries").doc(docName);
  //   print('DateSummary path: ${dateSummary.path}');
  //   dateSummary.get().then(
  //     (DocumentSnapshot doc) {
  //       _contents = doc.data() as Map<String, dynamic>;
  //       print('now its: ${_contents}');
  //       return true;
  //     },
  //     onError: (e) { 
  //       _error = 'No data found for the chosen date';
  //       return false;
  //     },
  //   );
  //   print('Contents are: ${_contents}');
  //   // return true;
  // }

  Future<bool> getDocument(String docName) async {
    final dateSummary = _db.collection("summaries").doc(docName);
    print('DateSummary path: ${dateSummary.path}');
    final DocumentSnapshot doc = await dateSummary.get().catchError((error) { _error = 'No data found for the chosen date'; });
    if (doc.exists) {
      _contents = doc.data() as Map<String, dynamic>;
      return true;
    } 
    return false;
  }

}


