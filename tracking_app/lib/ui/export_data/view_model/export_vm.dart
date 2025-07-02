import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

import 'package:Snacked/global.dart';


class ExportViewModel extends ChangeNotifier{
  String _jsonString = '';

  String get jsonString => _jsonString;
  
  Future<bool> getJSON() async {
    if (await storeRepo.fetchUserData(authRepo.userID)) {
      _jsonString = jsonEncode(storeRepo.data);
      return true;
    }
    return false;
  }

  Future<void> exportData() async{
    final saveLocation = await getApplicationDocumentsDirectory();
    final path = '${saveLocation.path}/your_snacked_data.json';
    final saveFile = File(path);
    await saveFile.writeAsString(_jsonString);
    await SharePlus.instance.share(ShareParams(files: [XFile(saveFile.path, mimeType: 'application/json')]));
  }

}


