import 'package:flutter/material.dart';

import 'package:snacktrac/data/repositories/auth_repository.dart';


class ProfileViewModel extends ChangeNotifier{
  final AuthRepository authRepo = AuthRepository();

  Future<String?> signOut() async {
    try {
      final status = await authRepo.signOut();
      return status;
    } catch (e) {
      return e.toString();
    }
  }
  
}

