import 'package:firebase_auth/firebase_auth.dart';



class AuthRepository {
  final _auth = FirebaseAuth.instance;

  User? get currentUser => _auth.currentUser!;
  Stream<User?> get userChanges => _auth.userChanges();

  Future<String?> register(String email, String password) async {
    try {
      UserCredential credential = await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      return 'Success';
    } on FirebaseAuthException catch (e) {
      if (e.code == 'invalid-email') {
        return 'Not a valid email format';
      } else if (e.code == 'email-already-in-use') {
        return 'An account is already associated with this email';
      } else if (e.code == 'weak-password') {
        return('Chosen password is too weak');
      } 
    } catch (e) {
        return e.toString();
      }
    return '';
  }

  Future<String?> login(String email, String password) async {
    try {
      UserCredential credential = await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      return 'Success';
    } on FirebaseAuthException catch (e) {
      if (e.code == 'invalid-email') {
        return 'Not a valid email format';
      } else if (e.code == 'invalid-credential') {
        return 'Invalid email or password';
      } 
    } catch (e) {
        return e.toString();
      }
    return '';
  }

  Future<void> signOut () async {
    await _auth.signOut();
  }

}

