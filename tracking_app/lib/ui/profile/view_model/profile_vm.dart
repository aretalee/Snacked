import 'package:flutter/material.dart';

import 'package:snacktrac/global.dart';


class ProfileViewModel extends ChangeNotifier{

  String? getName() {
    return authRepo.currentUser?.displayName;
  }

  Future<String?> signOut() async {
    try {
      final status = await authRepo.signOut();
      return status;
    } catch (e) {
      return e.toString();
    }
  }
  
}

