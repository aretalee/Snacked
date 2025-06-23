import 'package:flutter/material.dart';

import 'package:snacktrac/ui/navigation_bar/view_model/navigation_bar_vm.dart';



class NavBar extends StatefulWidget {
  const NavBar({super.key, required this.viewModel});
  final NavBarViewModel viewModel;

  @override
  State<NavBar> createState() => _NavBarState();
}


class _NavBarState extends State<NavBar> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: NavigationBar(
        selectedIndex: widget.viewModel.pageIndex,
        onDestinationSelected: (int index) {
          setState(() {widget.viewModel.pageSelected(index);} );
        },
        destinations: [
          NavigationDestination(
            icon: Icon(Icons.auto_graph_outlined),
            selectedIcon: Icon(Icons.auto_graph),
            label: 'Summary',
          ),
          NavigationDestination(
            icon: Icon(Icons.folder_open_outlined),
            selectedIcon: Icon(Icons.folder),
            label: 'Archive',
          ),
          NavigationDestination(
            icon: Icon(Icons.face_outlined),
            selectedIcon: Icon(Icons.face),
            label: 'Profile',
          ),
        ],
      ),
      body: widget.viewModel.currentPage,
    );
  }

}






