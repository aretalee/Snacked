import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import 'package:snacktrac/ui/archive/view_model/archive_vm.dart';


class PastSummaryPage extends StatefulWidget {
  const PastSummaryPage({super.key, required this.viewModel});
  final ArchiveViewModel viewModel;

  @override
  State<PastSummaryPage> createState() => _PastSummaryPageState();
}


class _PastSummaryPageState extends State<PastSummaryPage> {

  @override
  Widget build(BuildContext context) {
    return Scaffold (
      appBar: AppBar(
        title: Text('Summary for ${DateFormat('MMMM d, y').format(widget.viewModel.date)} ', 
        style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)), backgroundColor: Colors.black, 
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new),
          onPressed: () => context.go('/archive'),
        )
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('You spent:', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:15),
                    Text('Approximately ${widget.viewModel.eating} min eating', style: TextStyle(fontSize: 20)),
                    Text('${widget.viewModel.snacking} min were likely to be snacking', style: TextStyle(fontSize: 20), textAlign: TextAlign.center),
                    const SizedBox(height:30),
                    Text('Compared to yesterday:', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:15),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(widget.viewModel.comparison, style: TextStyle(fontSize: 20)), // need to figure out logic icon
                        const SizedBox(width:5),
                        widget.viewModel.compIcon ? Icon(Icons.arrow_downward, color: Colors.green, size: 20,) 
                        : Icon(Icons.arrow_upward, color: Colors.red, size: 20,) 
                      ]
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height:15),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('Based on your goals:', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:15),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(widget.viewModel.onTrack, style: TextStyle(fontSize: 20)), // need to figure out logic icon
                        const SizedBox(width:10),
                        widget.viewModel.compIcon ? Icon(Icons.thumb_up, color: Colors.green, size: 20,) 
                        : Icon(Icons.warning, color: Colors.blue, size: 20,)
                      ]
                    ),
                  ]
                ),
              ),
            ),
            const SizedBox(height:15),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('Anything that contributed to snacking?', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:15),
                    TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: widget.viewModel.comments,
                      ),
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





