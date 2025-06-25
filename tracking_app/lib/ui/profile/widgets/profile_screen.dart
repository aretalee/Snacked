import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:snacktrac/ui/profile/view_model/profile_vm.dart';


class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key, required this.viewModel});
  final ProfileViewModel viewModel;

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {

  @override
  Widget build(BuildContext context) {
    return Scaffold (
      appBar: AppBar(backgroundColor: Colors.black, automaticallyImplyLeading:false),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            CircleAvatar(
              radius:50,
              backgroundColor: Colors.white,
              child: CircleAvatar(
                radius:45,
                child: Icon(Icons.person_2_outlined, color: Colors.white, size: 50,)
              )
            ),
            const SizedBox(height:15),
            Text('${widget.viewModel.getName()}', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
            const SizedBox(height:45),
            FilledButton(
              onPressed: () => context.go('/profile/setGoals'),
              child: const Text('Set Daily Goal'), 
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () => context.go('/profile/export'), 
              child: const Text('Export Data'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () => context.go('/profile/changeUsername'),
              child: const Text('Change Username'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () => context.go('/profile/changePassword'),
              child: const Text('Change Password'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () => context.go('/profile/info'),
              child: const Text('About SnackTrac'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () async {
                final signOutStatus = await widget.viewModel.signOut();
                if (signOutStatus != null && signOutStatus.contains('Success')) {
                  context.go('/signin');
                };
              }, 
              child: const Text('Sign Out'),
            ),
          ],
        )
      )
    );
  }

}