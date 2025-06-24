import 'package:flutter/material.dart';

import 'package:snacktrac/ui/change_username/view_model/change_username_vm.dart';
import 'package:snacktrac/ui/profile/widgets/profile_screen.dart';
import 'package:snacktrac/ui/profile/view_model/profile_vm.dart';


class ChangeNamePage extends StatefulWidget {
  const ChangeNamePage({super.key, required this.viewModel});
  final ChangeNameViewModel viewModel;

  @override
  State<ChangeNamePage> createState() => _ChangeNamePageState();
}

class _ChangeNamePageState extends State<ChangeNamePage> {
  final TextEditingController _nameController = TextEditingController();
  String? _nameError;

  @override
  void initState() {
    super.initState();
  }

  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  Widget build(BuildContext context) {
    return Scaffold (
      appBar: AppBar(backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(30.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('Change Username', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,)),
                  const SizedBox(height:30),
                    TextField(
                      controller: _nameController,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'New username: ',
                        errorText: _nameError,
                      ),
                    ),
                    const SizedBox(height:30),
                    FilledButton(
                      onPressed: () async {
                        setState(() {
                        if (_nameController.text.isEmpty) {
                          _nameError = 'Please enter a username';
                        } else { _nameError = null; }
                      });
                      if (_nameError == null) {
                        widget.viewModel.setNewName(_nameController.text);
                        final nameChangeStatus = await widget.viewModel.changeUsername();
                        if (nameChangeStatus != null && nameChangeStatus.contains('Success')) {
                           ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('Successfully changed username', style: TextStyle(fontSize: 16, color:Colors.green, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 3),
                            )
                          );
                          Navigator.push(
                            context, MaterialPageRoute(builder: (context) => ProfilePage(viewModel: ProfileViewModel())),
                          );
                        } else{
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('$nameChangeStatus', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 3),
                            )
                          );
                        };
                      };
                    }, 
                    child: const Text('Confirm'),
                  ),
                ]
              )
            )
          )
        )
      )
    );
  }
  
}



