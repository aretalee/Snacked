import 'package:flutter/material.dart';

import 'package:Snacked/global.dart';


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

  Future<bool> status() async {
    final signOutStatus = await signOut();
     if (signOutStatus != null && signOutStatus.contains('Success')) {
        return true;
     } else { return false; }
  }
}

