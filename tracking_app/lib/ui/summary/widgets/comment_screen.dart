import 'package:flutter/material.dart';

import 'package:Snacked/ui/summary/view_model/summary_vm.dart';


class CommentPage extends StatelessWidget {
  const CommentPage({super.key, required this.viewModel});
  final SummaryViewModel viewModel;

  @override
  Widget build(BuildContext context) {
    final TextEditingController commentsController = TextEditingController();

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
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text('Anything that contributed to snacking?', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                  const SizedBox(height:15),
                  TextField(
                    controller: commentsController,
                    decoration: InputDecoration(
                      border: OutlineInputBorder(),
                      hintText: 'Type here: ',
                    ),
                   ),
                  const SizedBox(height:15),
                  FilledButton(
                    onPressed: () async {
                      if (await viewModel.updateComments(commentsController.text)) {
                        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('Commment saved.', style: TextStyle(fontSize: 16, color:Colors.green, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 1),
                          )
                        );
                      } else  {
                        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('Unable to save comment.', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 1),
                          )
                        );
                      }
                    }, 
                    child: const Text('Save'),
                  ),
                  const SizedBox(height:5),
                  FilledButton(
                    onPressed: () async {
                      final savedComment = await viewModel.comment;
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                        content: Text(savedComment, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                        duration: const Duration(seconds: 2),
                      ));
                    }, 
                    child: const Text('See comment'),
                  ),
                ]
              ),
            ),
          )
        )
      )
    );
  }
}


