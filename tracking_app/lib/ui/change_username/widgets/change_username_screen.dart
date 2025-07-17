import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:Snacked/ui/change_username/view_model/change_username_vm.dart';


class ChangeNamePage extends StatefulWidget {
  const ChangeNamePage({super.key, required this.viewModel});
  final ChangeNameViewModel viewModel;

  @override
  State<ChangeNamePage> createState() => _ChangeNamePageState();
}

class _ChangeNamePageState extends State<ChangeNamePage> {
  final TextEditingController _nameController = TextEditingController();

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  @override
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
                        errorText: widget.viewModel.nameError,
                      ),
                    ),
                    const SizedBox(height:30),
                    FilledButton(
                      onPressed: () async {
                        setState(() {
                        widget.viewModel.nameErrors(_nameController.text);
                      });
                      if (widget.viewModel.nameCheck(_nameController.text)) {
                        final nameChangeStatus = await widget.viewModel.changeUsername();
                        if (widget.viewModel.nameSuccess(nameChangeStatus)) {
                           ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('Successfully changed username', style: TextStyle(fontSize: 16, color:Colors.green, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 1),
                            )
                          );
                          context.go('/profile');
                        } else{
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('$nameChangeStatus', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 1),
                            )
                          );
                        }
                      }
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



