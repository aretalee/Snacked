import 'package:flutter/material.dart';

import 'package:snacktrac/ui/set_goals/widgets/set_goals_screen.dart';
import 'package:snacktrac/ui/export_data/widgets/export_screen.dart';
import 'package:snacktrac/ui/change_password/widgets/change_password_screen.dart';
import 'package:snacktrac/ui/change_username/widgets/change_username_screen.dart';
import 'package:snacktrac/ui/info/widgets/info_screen.dart';
import 'package:snacktrac/ui/change_password/view_model/change_password_vm.dart';
import 'package:snacktrac/ui/change_username/view_model/change_username_vm.dart';
import 'package:snacktrac/ui/sign_in_prompt/widgets/sign_in_prompt_screen.dart';
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
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const SetGoalsPage()),
                );
              }, 
              child: const Text('Set Daily Goal'), 
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const ExportPage()),
                );
              }, 
              child: const Text('Export Data'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => ChangeNamePage(viewModel: ChangeNameViewModel())),
                );
              }, 
              child: const Text('Change Username'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => ChangePwdPage(viewModel: ChangePwdViewModel())),
                );
              }, 
              child: const Text('Change Password'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const InfoPage()),
                );
              }, 
              child: const Text('About SnackTrac'),
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () async {
                final signOutStatus = await widget.viewModel.signOut();
                if (signOutStatus != null && signOutStatus.contains('Success')) {
                  Navigator.push(
                    context, MaterialPageRoute(builder: (context) => const SignInPage()),
                  );
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