import 'package:flutter/material.dart';


class NavBarViewModel extends ChangeNotifier{
  int pageIndex = 0;

  String get currentPage{
    switch (pageIndex) {
      case 0:
        return '/home';
      case 1:
       return '/archive';
      case 2:
        return '/profile';
      default:
        return '/home';
    }
  }

  void pageSelected(int index) {
    pageIndex = index;
    notifyListeners();
  }
}

