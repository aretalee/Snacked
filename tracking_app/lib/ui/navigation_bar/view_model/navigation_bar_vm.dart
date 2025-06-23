import 'package:flutter/material.dart';

import 'package:snacktrac/ui/home_page/widgets/home_page_screen.dart';
import 'package:snacktrac/ui/profile/widgets/profile_screen.dart';
import 'package:snacktrac/ui/archive/widgets/archive_screen.dart';



class NavBarViewModel extends ChangeNotifier{
  int pageIndex = 0;

  Widget get currentPage{
    switch (pageIndex) {
      case 0:
        return HomePage();
      case 1:
       return ArchivePage();
      case 2:
        return ProfilePage();
      default:
        return HomePage();
    }
  }

  void pageSelected(int index) {
    pageIndex = index;
    notifyListeners();
  }
}

