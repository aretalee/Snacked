import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/ui/summary/view_model/summary_vm.dart';
import 'package:Snacked/ui/archive/view_model/archive_vm.dart';

 
 class SummaryPage extends StatefulWidget {
  const SummaryPage({super.key, required this.viewModel, required this.viewModelA});
  final SummaryViewModel viewModel;
  final ArchiveViewModel viewModelA;

  @override
  State<SummaryPage> createState() => _SummaryPageState();
 }

class _SummaryPageState extends State<SummaryPage> {
  final TextEditingController _commentsController = TextEditingController();

  @override
  Widget build(BuildContext context) {
      return Scaffold (
        appBar: AppBar(
          title: Text('Summary for ${DateFormat('MMMM d, y').format(widget.viewModel.summaryDate)}', style: TextStyle(fontWeight: FontWeight.bold)), 
          backgroundColor: Colors.black, automaticallyImplyLeading:false),
        body: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Text('You spent:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height:10),
                      Text('Approximately ${widget.viewModelA.eating} min eating,', style: TextStyle(fontSize: 16), textAlign: TextAlign.center),
                      const SizedBox(height:5),
                      Text('${widget.viewModelA.snacking} min were likely to be snacking', style: TextStyle(fontSize: 16), textAlign: TextAlign.center),
                      const SizedBox(height:20),
                      Text('Compared to yesterday:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height:5),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(widget.viewModelA.comparison, style: TextStyle(fontSize: 16)), // need to figure out icon logic
                          const SizedBox(width:5),
                          (widget.viewModelA.compIcon && !widget.viewModelA.noDiff) ? Icon(Icons.arrow_downward, color: Colors.green, size: 20,) 
                          : (widget.viewModelA.noDiff ? Icon(Icons.swap_vert, color: Colors.white, size: 20,) 
                          : Icon(Icons.arrow_upward, color: Colors.red, size: 20,) )
                        ]
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height:10),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Text('Based on your goals:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height:5),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(widget.viewModelA.onTrack, style: TextStyle(fontSize: 16)), 
                          const SizedBox(width:10),
                          (widget.viewModelA.progressIcon) ? Icon(Icons.thumb_up, color: Colors.green, size: 20,) 
                          : Icon(Icons.warning, color: Colors.blue, size: 20,)
                        ]
                      ),
                    ]
                  ),
                ),
              ),
              const SizedBox(height:10),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Text('Anything that contributed to snacking?', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                      const SizedBox(height:10),
                      TextField(
                        controller: _commentsController,
                        decoration: InputDecoration(
                          border: OutlineInputBorder(),
                          hintText: 'Type here: ',
                        ),
                      ),
                      const SizedBox(height:10),
                      FilledButton(
                        onPressed: () async {
                          if (await widget.viewModel.updateComments(_commentsController.text)) {
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
                          final savedComment = await widget.viewModel.comment;
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                            content: Text('$savedComment', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                            duration: const Duration(seconds: 2),
                          ));
                        }, 
                        child: const Text('See comment'),
                      ),
                    ]
                  ),
                ),
              ),
            ],
          )
        )
      );

  }

}





